"""模评云本地服务：静态工作台 + CUMCM 诊断 API。"""

from __future__ import annotations

import argparse
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, message=".*'cgi' is deprecated.*")
import cgi
import json
import mimetypes
import os
import shutil
import tempfile
import threading
import uuid
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from modelscore.engine import run_review
from modelscore.parser import parse_material
from modelscore.reporting import save_json, save_pdf
from modelscore.corpus import case_detail, list_cases, run_corpus_quality, update_review
from modelscore.storage import get_job, init_db, list_workflows, save_job, sync_workflows


ROOT = Path(__file__).resolve().parent
TASKS = ROOT / "data" / "tasks"
MAX_UPLOAD = 120 * 1024 * 1024
JOBS: dict[str, dict] = {}
JOBS_LOCK = threading.Lock()
ALLOWED = {
    "problem": {".pdf", ".docx", ".txt"},
    "paper": {".pdf", ".docx", ".txt"},
    "code": {".zip", ".py", ".m", ".ipynb", ".txt"},
    "extra": {".pdf", ".docx", ".txt", ".zip", ".csv", ".json"},
}


def _safe_name(name: str) -> str:
    return Path(unquote(name or "upload.bin").replace("\\", "/")).name


def _set_job(job_id: str, **changes):
    with JOBS_LOCK:
        current = JOBS.get(job_id) or get_job(job_id) or {}
        current.update(changes)
        JOBS[job_id] = current
        save_job(job_id, current)


def _get_job(job_id: str) -> dict:
    with JOBS_LOCK:
        current = JOBS.get(job_id)
    return dict(current or get_job(job_id) or {})


def _save_form(form, target: Path) -> tuple[dict, dict[str, Path]]:
    task = {
        "contest": form.getfirst("contest", "CUMCM"), "problem": form.getfirst("problem_id", "B"),
        "group": form.getfirst("group", "本科生组"), "region": form.getfirst("region", ""),
        "mode": form.getfirst("mode", "during"), "review_mode": form.getfirst("review_mode", "strict"),
    }
    if "CUMCM" not in task["contest"] and "国赛" not in task["contest"]:
        raise ValueError("当前真实评分 MVP 仅支持 CUMCM 国赛")
    if not task["region"]:
        raise ValueError("CUMCM 任务必须选择赛区")
    target.mkdir(parents=True, exist_ok=True)
    paths = {}
    for slot in ("problem", "paper", "code", "extra"):
        item = form[slot] if slot in form else None
        if item is None or not getattr(item, "filename", None):
            if slot in {"problem", "paper", "code"}:
                raise ValueError(f"缺少必需文件：{slot}")
            continue
        name = _safe_name(item.filename)
        suffix = Path(name).suffix.lower()
        if suffix not in ALLOWED[slot]:
            raise ValueError(f"{slot} 不支持 {suffix} 格式")
        path = target / f"{slot}-{name}"
        with path.open("wb") as output:
            shutil.copyfileobj(item.file, output, length=1024 * 1024)
        paths[slot] = path
    return task, paths


def _execute(task: dict, paths: dict[str, Path], job_id: str | None = None) -> dict:
    if job_id:
        _set_job(job_id, status="parsing", progress=25, message="正在解析材料")
    parsed = {slot: parse_material(path, slot) for slot, path in paths.items()}
    if job_id:
        _set_job(job_id, status="reviewing", progress=55, message="正在执行 42 项规则与模型复核")
    report = run_review(task, parsed["problem"], parsed["paper"], parsed.get("code"))
    if job_id:
        _set_job(job_id, status="reporting", progress=85, message="正在生成报告")
    task_dir = TASKS / report["report_id"]
    task_dir.mkdir(parents=True, exist_ok=True)
    report["downloads"] = {
        "json": f"/api/reports/{report['report_id']}/report.json", "pdf": f"/api/reports/{report['report_id']}/report.pdf",
    }
    save_json(report, task_dir / "report.json")
    save_pdf(report, task_dir / "report.pdf")
    return report


def _run_job(job_id: str, task: dict, paths: dict[str, Path], upload_dir: Path):
    try:
        report = _execute(task, paths, job_id)
        _set_job(job_id, status="completed", progress=100, message="诊断完成", report=report)
    except Exception as exc:
        _set_job(job_id, status="failed", progress=100, message="评审失败", error=str(exc)[:500])
    finally:
        shutil.rmtree(upload_dir, ignore_errors=True)


class Handler(SimpleHTTPRequestHandler):
    server_version = "ModelScore/0.5"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _json(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path.startswith("/data/"):
            return self._json(HTTPStatus.FORBIDDEN, {"error": "本地数据不允许通过静态服务器直接访问"})
        if parsed.path == "/api/health":
            return self._json(200, {
                "status": "ok", "version": "0.5.0", "storage": "sqlite", "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
                "openai_status": "configured-not-validated" if os.getenv("OPENAI_API_KEY") else "disabled",
                "model": os.getenv("OPENAI_MODEL", "gpt-5.6-luna") if os.getenv("OPENAI_API_KEY") else None,
            })
        if parsed.path == "/api/workflows":
            return self._json(200, {"workflows": list_workflows()})
        if parsed.path == "/api/corpus":
            return self._json(200, list_cases())
        if parsed.path == "/api/corpus/quality":
            quality_path = ROOT / "research" / "corpus_quality_report.json"
            if not quality_path.exists():
                return self._json(200, {"status": "not-run", "cases": [], "summary": {}})
            return self._json(200, json.loads(quality_path.read_text(encoding="utf-8")))
        if parsed.path.startswith("/api/corpus/"):
            case_id = parsed.path.removeprefix("/api/corpus/").strip("/")
            if not case_id or "/" in case_id:
                return self._json(404, {"error": "语料案例地址无效"})
            try:
                return self._json(200, case_detail(case_id))
            except KeyError:
                return self._json(404, {"error": "语料案例不存在"})
        if parsed.path.startswith("/api/jobs/"):
            job_id = parsed.path.rsplit("/", 1)[-1]
            job = _get_job(job_id)
            if not job:
                return self._json(404, {"error": "任务不存在或服务已重启"})
            return self._json(200, {"job_id": job_id, **job})
        if parsed.path.startswith("/api/reports/"):
            parts = parsed.path.strip("/").split("/")
            if len(parts) != 4 or parts[0] != "api" or parts[1] != "reports":
                return self._json(404, {"error": "报告地址无效"})
            report_id, filename = parts[2], parts[3]
            if not report_id.replace("-", "").isalnum() or filename not in {"report.json", "report.pdf"}:
                return self._json(404, {"error": "报告不存在"})
            target = TASKS / report_id / filename
            if not target.exists():
                return self._json(404, {"error": "报告不存在"})
            data = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(filename)[0] or "application/octet-stream")
            self.send_header("Content-Disposition", f'attachment; filename="{report_id}-{filename}"')
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            return self.wfile.write(data)
        return super().do_GET()

    def do_POST(self):
        endpoint = urlparse(self.path).path
        if endpoint == "/api/workflows/sync":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 8 * 1024 * 1024:
                    return self._json(413, {"error": "工作流数据大小无效"})
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                workflows = sync_workflows(payload.get("workflows"))
                return self._json(200, {"workflows": workflows, "count": len(workflows)})
            except (ValueError, json.JSONDecodeError, AttributeError) as exc:
                return self._json(400, {"error": str(exc)})
        if endpoint == "/api/corpus/quality":
            try:
                return self._json(200, run_corpus_quality())
            except Exception as exc:
                return self._json(500, {"error": "批量质检失败", "detail": str(exc)[:500]})
        if endpoint.startswith("/api/corpus/") and endpoint.endswith("/review"):
            case_id = endpoint.removeprefix("/api/corpus/").removesuffix("/review").strip("/")
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 64 * 1024:
                    return self._json(413, {"error": "复核数据大小无效"})
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                return self._json(200, update_review(case_id, payload))
            except KeyError:
                return self._json(404, {"error": "语料案例不存在"})
            except (ValueError, json.JSONDecodeError) as exc:
                return self._json(400, {"error": str(exc)})
        if endpoint not in {"/api/reviews", "/api/jobs"}:
            return self._json(404, {"error": "接口不存在"})
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0 or content_length > MAX_UPLOAD:
            return self._json(413, {"error": "上传总大小必须小于 120 MB"})
        try:
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={
                "REQUEST_METHOD": "POST", "CONTENT_TYPE": self.headers.get("Content-Type", ""),
                "CONTENT_LENGTH": str(content_length),
            })
            if endpoint == "/api/jobs":
                job_id = "JOB-" + uuid.uuid4().hex[:12].upper()
                upload_dir = TASKS / ".uploads" / job_id
                task, paths = _save_form(form, upload_dir)
                _set_job(job_id, status="queued", progress=5, message="任务已创建")
                threading.Thread(target=_run_job, args=(job_id, task, paths, upload_dir), daemon=True).start()
                return self._json(202, {"job_id": job_id, "status": "queued", "progress": 5})
            with tempfile.TemporaryDirectory(prefix="modelscore-") as tmp:
                task, paths = _save_form(form, Path(tmp))
                return self._json(200, _execute(task, paths))
        except ValueError as exc:
            return self._json(400, {"error": str(exc)})
        except Exception as exc:
            return self._json(500, {"error": "评审执行失败", "detail": str(exc)[:500]})

    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {fmt % args}")


def main():
    parser = argparse.ArgumentParser(description="启动模评云本地评分服务")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4186)
    args = parser.parse_args()
    TASKS.mkdir(parents=True, exist_ok=True)
    init_db(recover_jobs=True)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"ModelScoreAgent running at http://{args.host}:{args.port}/app.html")
    print("OpenAI:", "enabled" if os.getenv("OPENAI_API_KEY") else "disabled (local rules fallback)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

"""Local corpus governance, anonymization review and quality checks."""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from .engine import run_review
from .parser import parse_material


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research" / "public_corpus_manifest.json"
DATA_ROOT = ROOT / "data" / "research_corpus"
REVIEWS_PATH = DATA_ROOT / "reviews.json"
QUALITY_PATH = ROOT / "research" / "corpus_quality_report.json"
REVIEWED_ROOT = DATA_ROOT / "reviewed"

PII_PATTERNS = (
    ("email", re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")),
    ("phone", re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)")),
    ("cn_id", re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\d)")),
    ("team_number", re.compile(r"(?im)^.*(?:参赛队号|报名号|队伍编号|赛号).*$")),
    ("school_or_author", re.compile(r"(?im)^.*(?:参赛学校|学校名称|所属学校|队员姓名|指导教师|作者姓名|学号).*$")),
)
REDACTION_LABELS = {
    "email": "[已删除邮箱]", "phone": "[已删除手机号]", "cn_id": "[已删除身份证号]",
    "team_number": "[已删除参赛队号]", "school_or_author": "[已删除身份信息]",
}


def _load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_manifest() -> dict:
    return _load_json(MANIFEST_PATH, {"count": 0, "records": [], "policy": {}})


def load_reviews() -> dict:
    return _load_json(REVIEWS_PATH, {"schema_version": 1, "cases": {}})


def _record(case_id: str) -> dict:
    for record in load_manifest().get("records", []):
        if record.get("case_id") == case_id:
            return record
    raise KeyError(case_id)


def _source_text(record: dict) -> tuple[Path, str]:
    path = ROOT / record["local_anonymized_text"]
    return path, path.read_text(encoding="utf-8", errors="replace")


def scan_pii(text: str) -> list[dict]:
    findings: list[dict] = []
    occupied: list[tuple[int, int]] = []
    for kind, pattern in PII_PATTERNS:
        for match in pattern.finditer(text):
            if any(match.start() < end and match.end() > start for start, end in occupied):
                continue
            line = text.count("\n", 0, match.start()) + 1
            excerpt_start = max(0, text.rfind("\n", 0, match.start()) + 1)
            excerpt_end = text.find("\n", match.end())
            if excerpt_end < 0:
                excerpt_end = min(len(text), match.end() + 80)
            fingerprint = hashlib.sha256(f"{kind}:{match.start()}:{match.group(0)}".encode("utf-8")).hexdigest()[:16]
            findings.append({
                "id": fingerprint, "kind": kind, "line": line,
                "excerpt": text[excerpt_start:excerpt_end][:240],
                "start": match.start(), "end": match.end(),
            })
            occupied.append((match.start(), match.end()))
    return sorted(findings, key=lambda item: item["start"])


def _code_inventory(record: dict) -> dict:
    archive_value = record.get("local_source_archive")
    archive = ROOT / archive_value if archive_value else None
    if not archive or not archive.exists():
        return {"status": "not-downloaded", "code_files": 0, "data_files": 0, "dependency_files": [], "run_guides": [], "random_seed_mentions": 0, "execution": "not-executed"}
    code_ext = {".py", ".m", ".r", ".jl", ".ipynb", ".cpp", ".c"}
    data_ext = {".csv", ".xlsx", ".xls", ".mat", ".json"}
    dependency_names = {"requirements.txt", "environment.yml", "environment.yaml", "pyproject.toml", "package.json", "renv.lock"}
    code_files, data_files, dependency_files, run_guides = [], [], [], []
    seed_mentions = 0
    with zipfile.ZipFile(archive) as bundle:
        for info in bundle.infolist()[:3000]:
            name = info.filename.replace("\\", "/")
            suffix = Path(name).suffix.lower()
            base = Path(name).name.lower()
            if suffix in code_ext:
                code_files.append(name)
                if info.file_size <= 2_000_000:
                    try:
                        body = bundle.read(info).decode("utf-8", errors="ignore")
                        seed_mentions += len(re.findall(r"(?i)(?:random[_.]?seed|np\.random\.seed|rng\s*\()", body))
                    except (KeyError, OSError):
                        pass
            if suffix in data_ext:
                data_files.append(name)
            if base in dependency_names:
                dependency_files.append(name)
            if base.startswith("readme"):
                run_guides.append(name)
    if code_files and (dependency_files or run_guides):
        status = "materials-present"
    elif code_files:
        status = "partial"
    else:
        status = "no-code-found"
    return {
        "status": status, "code_files": len(code_files), "data_files": len(data_files),
        "dependency_files": dependency_files[:20], "run_guides": run_guides[:20],
        "random_seed_mentions": seed_mentions,
        "sample_code_files": code_files[:15],
        "execution": "not-executed-untrusted-third-party-code",
    }


def case_detail(case_id: str) -> dict:
    record = dict(_record(case_id))
    _, text = _source_text(record)
    findings = scan_pii(text)
    review = load_reviews().get("cases", {}).get(case_id, {"status": "pending", "notes": "", "actions": {}})
    for finding in findings:
        finding["action"] = review.get("actions", {}).get(finding["id"], "pending")
        finding.pop("start", None)
        finding.pop("end", None)
    record["review"] = review
    record["pii_findings"] = findings
    record["code_inventory"] = _code_inventory(record)
    record["model_upload_allowed"] = record.get("text_quality") == "usable" and review.get("status") == "approved"
    return record


def list_cases() -> dict:
    manifest = load_manifest()
    details = [case_detail(r["case_id"]) for r in manifest.get("records", [])]
    return {
        "generated_at": manifest.get("generated_at"), "policy": manifest.get("policy", {}),
        "stats": {
            "total": len(details),
            "usable": sum(d.get("text_quality") == "usable" for d in details),
            "ocr_required": sum(d.get("text_quality") == "ocr-required" for d in details),
            "approved": sum(d["review"].get("status") == "approved" for d in details),
            "with_code": sum(d["code_inventory"]["code_files"] > 0 for d in details),
            "award_verified": sum(d.get("award_evidence_status") == "officially-verified" for d in details),
        },
        "cases": details,
    }


def update_review(case_id: str, payload: dict) -> dict:
    record = _record(case_id)
    source_path, text = _source_text(record)
    findings = scan_pii(text)
    valid_ids = {item["id"] for item in findings}
    actions = payload.get("actions", {})
    if not isinstance(actions, dict) or any(k not in valid_ids or v not in {"redact", "false-positive", "pending"} for k, v in actions.items()):
        raise ValueError("匿名化处理项无效")
    status = payload.get("status", "pending")
    if status not in {"pending", "needs-redaction", "approved"}:
        raise ValueError("复核状态无效")
    if status == "approved" and any(actions.get(item["id"], "pending") == "pending" for item in findings):
        raise ValueError("仍有未处理的敏感信息候选项")
    reviewed = text
    for finding in reversed(scan_pii(text)):
        if actions.get(finding["id"]) == "redact":
            reviewed = reviewed[:finding["start"]] + REDACTION_LABELS[finding["kind"]] + reviewed[finding["end"]:]
    reviewed_path = REVIEWED_ROOT / case_id / "paper.txt"
    reviewed_path.parent.mkdir(parents=True, exist_ok=True)
    reviewed_path.write_text(reviewed, encoding="utf-8")
    reviews = load_reviews()
    entry = {
        "status": status, "notes": str(payload.get("notes", ""))[:2000], "actions": actions,
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "reviewed_text": str(reviewed_path.relative_to(ROOT).as_posix()),
    }
    reviews.setdefault("cases", {})[case_id] = entry
    _write_json(REVIEWS_PATH, reviews)
    return case_detail(case_id)


def run_corpus_quality() -> dict:
    cases = []
    old_key = os.environ.pop("OPENAI_API_KEY", None)
    try:
        for record in load_manifest().get("records", []):
            if record.get("text_quality") != "usable":
                cases.append({"case_id": record["case_id"], "status": "skipped", "reason": "text-not-usable"})
                continue
            started = time.perf_counter()
            paper = parse_material(ROOT / record["local_anonymized_text"], "paper")
            problem = parse_material(ROOT / record["local_problem"], "problem")
            report = run_review({"contest": "CUMCM", "problem": record["problem_id"], "group": "本科生组", "region": "公开语料", "mode": "evaluation"}, problem, paper, None)
            valid_evidence = 0
            cited = 0
            for check in report["checks"]:
                evidence = check.get("evidence")
                if evidence:
                    cited += 1
                    quote = evidence.get("quote", "")
                    normalized_quote = re.sub(r"\s+", " ", quote).strip()
                    normalized_paper = re.sub(r"\s+", " ", paper.text)
                    valid_evidence += bool(
                        normalized_quote
                        and (normalized_quote in normalized_paper or quote.startswith("自动结构检查"))
                        and isinstance(evidence.get("page"), int)
                    )
            cases.append({
                "case_id": record["case_id"], "status": "passed" if len(report["checks"]) == 42 else "failed",
                "checks": len(report["checks"]), "cited_checks": cited,
                "evidence_exact_match_rate": round(valid_evidence / max(cited, 1), 4),
                "warnings": report.get("warnings", []), "elapsed_ms": round((time.perf_counter() - started) * 1000),
                "provider": report["provider"], "score_is_unlabeled_diagnostic_only": report["score"],
            })
    finally:
        if old_key is not None:
            os.environ["OPENAI_API_KEY"] = old_key
    payload = {
        "schema_version": 1, "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "unlabeled pipeline quality; not model accuracy or teacher agreement",
        "cases": cases,
        "summary": {
            "total": len(cases), "processed": sum(c["status"] != "skipped" for c in cases),
            "passed": sum(c["status"] == "passed" for c in cases), "skipped": sum(c["status"] == "skipped" for c in cases),
        },
    }
    _write_json(QUALITY_PATH, payload)
    return payload

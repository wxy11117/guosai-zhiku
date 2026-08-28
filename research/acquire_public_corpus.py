"""Download a small, traceable public CUMCM research corpus.

Raw files stay in data/research_corpus (git-ignored).  The script produces
an anonymized text copy, a provenance manifest, and an empty teacher-label
queue.  Public availability is not treated as permission to redistribute.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data" / "research_corpus"
RAW_ROOT = DATA_ROOT / "raw"
ANON_ROOT = DATA_ROOT / "anonymized"
OCR_ROOT = DATA_ROOT / "ocr"
MANIFEST_PATH = ROOT / "research" / "public_corpus_manifest.json"
QUEUE_PATH = ROOT / "evals" / "public-corpus-annotation-queue.jsonl"
USER_AGENT = "ModelScore-Corpus-Builder/1.0 (local research dataset)"


@dataclass(frozen=True)
class Source:
    case_id: str
    year: int
    problem_id: str
    award_claim: str
    repo: str
    branch: str
    license_spdx: str
    paper_path: str
    problem_path: str | None = None
    source_text_path: str | None = None
    official_problem_archive: tuple[str, str] | None = None
    rights_note: str = "Repository license recorded; keep raw files local and verify scope before redistribution."


SOURCES = (
    Source(
        "cumcm-2022-b-national-second",
        2022,
        "B",
        "全国二等奖（作者仓库自述，待官方名单逐项核验）",
        "aasdl1/CUMCM2022-B",
        "main",
        "Apache-2.0",
        "Solutions-无人机编队飞行中的纯方位无源定位模型研究.pdf",
        "Problems-B题.pdf",
    ),
    Source(
        "cumcm-2022-c-national-second",
        2022,
        "C",
        "全国二等奖（作者仓库自述，待官方名单逐项核验）",
        "shannany0606/2022_National_Math_Modeling_Competiotion",
        "main",
        "MIT",
        "最终论文.pdf",
        "C题题目/C题.pdf",
    ),
    Source(
        "cumcm-2023-a-national-first",
        2023,
        "A",
        "全国一等奖（作者仓库自述，待官方名单逐项核验）",
        "linggm3/2023_CUMCM_National-First-Prize",
        "main",
        "MIT",
        "定日镜场优化设计模型.pdf",
        "A题.pdf",
    ),
    Source(
        "cumcm-2024-a-national-first",
        2024,
        "A",
        "全国一等奖及数模之星（作者仓库自述，待官方名单逐项核验）",
        "cny123222/CUMCM-2024A-Bench-Dragon",
        "main",
        "MIT",
        "OurPaper.pdf",
        official_problem_archive=(
            "https://www.mcm.edu.cn/upload_cn/node/725/pmkWxf8H9cfe9984c1a1a5b1263e5dd3b5596ed5.zip",
            "A",
        ),
    ),
    Source(
        "cumcm-2025-b-national-first",
        2025,
        "B",
        "全国一等奖（作者仓库自述，待官方名单逐项核验）",
        "CUMCM-2025B-Team/CUMCM-2025-Problem-B",
        "main",
        "MIT",
        "25_国赛/main.pdf",
        "题目以及原始数据/B题.pdf",
        "25_国赛/main.tex",
        rights_note="Repository has an MIT file, while its README contains separate paper/data caveats; local research use only pending review.",
    ),
    Source(
        "cumcm-2025-c-provincial-first",
        2025,
        "C",
        "山东省一等奖（作者仓库自述，待赛区名单逐项核验）",
        "xueqiyuan586-boop/CUMCM-NIPT-Modeling",
        "main",
        "MIT",
        "paper/NIPT_Modeling_Paper.pdf",
        official_problem_archive=(
            "https://www.mcm.edu.cn/upload_cn/node/759/SvpohSGacdffe718bcaa3b6e835c03ae3461cab1.zip",
            "C",
        ),
    ),
    Source(
        "cumcm-2025-b-jiangsu-third",
        2025,
        "B",
        "江苏省三等奖（作者仓库自述，待赛区名单逐项核验）",
        "Skyler-Luo/CUMCM2025-B",
        "main",
        "MIT",
        "paper.pdf",
        "topic-B.pdf",
        rights_note="Repository is MIT-licensed and contains paper, problem, code, and data; keep a local research copy and verify paper-license scope before redistribution.",
    ),
)


IDENTITY_LINE = re.compile(
    r"(?im)^.*(?:参赛队号|参赛学校|所属学校|学校名称|队员姓名|指导教师|作者姓名|报名号|学号).*$"
)
EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
PHONE = re.compile(r"(?<!\d)(?:\+?86[- ]?)?1[3-9]\d{9}(?!\d)")
CN_ID = re.compile(r"(?<!\d)\d{17}[0-9Xx](?!\d)")


def raw_url(source: Source, remote_path: str) -> str:
    encoded = urllib.parse.quote(remote_path, safe="/")
    return f"https://raw.githubusercontent.com/{source.repo}/{source.branch}/{encoded}"


def archive_url(source: Source) -> str:
    return f"https://github.com/{source.repo}/archive/refs/heads/{urllib.parse.quote(source.branch, safe='')}.zip"


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=90) as response, destination.open("wb") as output:
        shutil.copyfileobj(response, output)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_official_problem(archive: Path, problem_id: str, destination: Path) -> str:
    with zipfile.ZipFile(archive) as bundle:
        pdf_names = [name for name in bundle.namelist() if name.lower().endswith(".pdf")]
        markers = (f"{problem_id}题", f"{problem_id} 題", f"Problem {problem_id}")
        matches = [name for name in pdf_names if any(marker.lower() in name.lower() for marker in markers)]
        if not matches:
            matches = [name for name in pdf_names if Path(name).stem.upper() == problem_id]
        if not matches:
            raise RuntimeError(f"Official archive has no identifiable {problem_id} problem PDF: {pdf_names}")
        selected = sorted(matches, key=len)[0]
        destination.parent.mkdir(parents=True, exist_ok=True)
        with bundle.open(selected) as source_handle, destination.open("wb") as output:
            shutil.copyfileobj(source_handle, output)
        return selected


def extract_pdf_text(path: Path) -> tuple[str, int]:
    reader = PdfReader(str(path))
    pages = [(page.extract_text() or "") for page in reader.pages]
    return "\n\n".join(pages), len(pages)


def anonymize(text: str) -> tuple[str, dict[str, int]]:
    counts = {
        "identity_lines": len(IDENTITY_LINE.findall(text)),
        "emails": len(EMAIL.findall(text)),
        "phones": len(PHONE.findall(text)),
        "cn_ids": len(CN_ID.findall(text)),
    }
    result = IDENTITY_LINE.sub("[已删除身份信息]", text)
    result = EMAIL.sub("[已删除邮箱]", result)
    result = PHONE.sub("[已删除手机号]", result)
    result = CN_ID.sub("[已删除身份证号]", result)
    return result, counts


def readable_text_ratio(text: str) -> float:
    non_space = re.findall(r"\S", text)
    if not non_space:
        return 0.0
    readable = re.findall(r"[\u4e00-\u9fffA-Za-z0-9]", text)
    return round(len(readable) / len(non_space), 4)


def cjk_text_ratio(text: str) -> float:
    non_space = re.findall(r"\S", text)
    if not non_space:
        return 0.0
    cjk = re.findall(r"[\u4e00-\u9fff]", text)
    return round(len(cjk) / len(non_space), 4)


def replace_invalid_unicode(text: str) -> tuple[str, int]:
    invalid = sum(0xD800 <= ord(char) <= 0xDFFF for char in text)
    if invalid:
        text = text.encode("utf-8", errors="replace").decode("utf-8")
    return text, invalid


def annotation_record(source: Source, paper_text_path: Path, problem_path: Path) -> dict:
    relative_paper = Path("..") / paper_text_path.relative_to(ROOT)
    relative_problem = Path("..") / problem_path.relative_to(ROOT)
    return {
        "case_id": source.case_id,
        "teacher_annotation_status": "unlabeled",
        "paper": relative_paper.as_posix(),
        "problem": relative_problem.as_posix(),
        "code": None,
        "problem_id": source.problem_id,
        "group": "本科生组",
        "region": None,
        "teacher_dimensions": {
            "假设合理性": None,
            "建模创新性": None,
            "结果正确性": None,
            "表述清晰性": None,
            "代码可复现性": None,
            "图文美观性": None,
        },
        "teacher_high_risk_rule_ids": [],
        "notes": "公开样本；自动匿名化后仍须人工复核。获奖等级不是教师维度分数。",
    }


def acquire(force: bool = False) -> dict:
    records: list[dict] = []
    queue: list[dict] = []
    for source in SOURCES:
        raw_case = RAW_ROOT / source.case_id
        anon_case = ANON_ROOT / source.case_id
        paper_path = raw_case / "paper.pdf"
        problem_path = raw_case / "problem.pdf"
        readme_path = raw_case / "README.md"
        license_path = raw_case / "LICENSE"
        source_text_path = raw_case / "paper-source.txt"
        source_archive_path = raw_case / "source.zip"

        for remote, local in ((source.paper_path, paper_path), ("README.md", readme_path), ("LICENSE", license_path)):
            if force or not local.exists():
                download(raw_url(source, remote), local)

        if source.source_text_path and (force or not source_text_path.exists()):
            download(raw_url(source, source.source_text_path), source_text_path)

        if force or not source_archive_path.exists():
            try:
                download(archive_url(source), source_archive_path)
            except Exception as exc:
                print(f"warning: source archive unavailable for {source.case_id}: {exc}", file=sys.stderr)

        official_member = None
        if source.problem_path:
            if force or not problem_path.exists():
                download(raw_url(source, source.problem_path), problem_path)
            problem_source_url = raw_url(source, source.problem_path)
        elif source.official_problem_archive:
            archive_url, problem_id = source.official_problem_archive
            archive_path = RAW_ROOT / "_official" / f"cumcm-{source.year}-problems.zip"
            if force or not archive_path.exists():
                download(archive_url, archive_path)
            if force or not problem_path.exists():
                official_member = extract_official_problem(archive_path, problem_id, problem_path)
            problem_source_url = archive_url
        else:
            raise RuntimeError(f"No problem source for {source.case_id}")

        pdf_text, pages = extract_pdf_text(paper_path)
        pdf_cjk_ratio = cjk_text_ratio(pdf_text)
        ocr_text_path = OCR_ROOT / source.case_id / "paper.txt"
        if ocr_text_path.exists():
            paper_text = ocr_text_path.read_text(encoding="utf-8", errors="replace")
            extraction_method = "local-rapidocr"
        elif source.source_text_path and pdf_cjk_ratio < 0.05:
            paper_text = source_text_path.read_text(encoding="utf-8", errors="replace")
            extraction_method = "repository-source-text-fallback"
        else:
            paper_text = pdf_text
            extraction_method = "pypdf"
        paper_text, invalid_unicode_replacements = replace_invalid_unicode(paper_text)
        text_ratio = readable_text_ratio(paper_text)
        cjk_ratio = cjk_text_ratio(paper_text)
        text_quality = "usable" if cjk_ratio >= 0.05 and len(paper_text) >= 1_000 else "ocr-required"
        anonymized, redaction_counts = anonymize(paper_text)
        anon_case.mkdir(parents=True, exist_ok=True)
        paper_text_path = anon_case / "paper.txt"
        paper_text_path.write_text(anonymized, encoding="utf-8")

        records.append(
            {
                "case_id": source.case_id,
                "year": source.year,
                "problem_id": source.problem_id,
                "award_claim": source.award_claim,
                "award_evidence_status": "author-repository-claim; official-verification-pending",
                "official_award_list_index": "https://www.mcm.edu.cn/html_cn/block/018500ec1a6bd8c7e9997133def2b590.html",
                "award_verification_note": "官方历年名单入口已定位；公开仓库缺少可可靠关联到官方队伍的唯一标识，暂不把仓库自述升级为官方核验。",
                "repository": f"https://github.com/{source.repo}",
                "repository_license_spdx": source.license_spdx,
                "rights_note": source.rights_note,
                "paper_source_url": raw_url(source, source.paper_path),
                "problem_source_url": problem_source_url,
                "official_archive_member": official_member,
                "local_raw_paper": str(paper_path.relative_to(ROOT).as_posix()),
                "local_problem": str(problem_path.relative_to(ROOT).as_posix()),
                "local_anonymized_text": str(paper_text_path.relative_to(ROOT).as_posix()),
                "local_source_archive": str(source_archive_path.relative_to(ROOT).as_posix()) if source_archive_path.exists() else None,
                "paper_sha256": sha256(paper_path),
                "problem_sha256": sha256(problem_path),
                "paper_pages": pages,
                "extracted_characters": len(paper_text),
                "extraction_method": extraction_method,
                "invalid_unicode_replacements": invalid_unicode_replacements,
                "readable_text_ratio": text_ratio,
                "cjk_text_ratio": cjk_ratio,
                "text_quality": text_quality,
                "automatic_redactions": redaction_counts,
                "anonymization_status": "manual-review-required",
                "teacher_annotation_status": "unlabeled",
                "redistribution": "disabled; local research copy only",
            }
        )
        if text_quality == "usable":
            queue.append(annotation_record(source, paper_text_path, problem_path))

    manifest = {
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "policy": {
            "purpose": "local evaluation and annotation recruitment",
            "raw_files_committed": False,
            "public_availability_is_not_redistribution_permission": True,
            "manual_anonymization_review_required_before_model_upload": True,
            "award_claims_are_not_teacher_scores": True,
        },
        "count": len(records),
        "annotation_ready_count": len(queue),
        "records": records,
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(
        "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in queue), encoding="utf-8"
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="redownload existing files")
    args = parser.parse_args()
    try:
        manifest = acquire(force=args.force)
    except Exception as exc:
        print(f"acquisition failed: {exc}", file=sys.stderr)
        return 1
    print(f"Prepared {manifest['count']} public cases")
    print(f"Manifest: {MANIFEST_PATH}")
    print(f"Teacher queue: {QUEUE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

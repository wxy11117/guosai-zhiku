"""对语料库中标记为 ocr-required 的论文执行本地中文 OCR。

OCR 只在本机运行，不上传论文内容。输出保留逐页定位标记，并写入
data/research_corpus/ocr/<case_id>/paper.txt，随后重新生成采集清单即可使用。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
from pdf2image import convert_from_path, pdfinfo_from_path
from rapidocr_onnxruntime import RapidOCR


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "research" / "public_corpus_manifest.json"
DATA_ROOT = ROOT / "data" / "research_corpus"
POPPLER = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "native" / "poppler" / "Library" / "bin"


def _page_text(result: list | None) -> str:
    if not result:
        return ""
    rows = sorted(result, key=lambda item: (min(p[1] for p in item[0]), min(p[0] for p in item[0])))
    return "\n".join(str(row[1]).strip() for row in rows if str(row[1]).strip())


def ocr_pdf(pdf_path: Path, output_path: Path, dpi: int = 170) -> dict:
    page_count = int(pdfinfo_from_path(str(pdf_path), poppler_path=str(POPPLER))["Pages"])
    engine = RapidOCR()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    chunks: list[str] = []
    recognized = 0
    for page_number in range(1, page_count + 1):
        image = convert_from_path(
            str(pdf_path), dpi=dpi, first_page=page_number, last_page=page_number,
            fmt="png", grayscale=False, thread_count=1, poppler_path=str(POPPLER),
        )[0]
        result, _ = engine(np.asarray(image.convert("RGB")))
        text = _page_text(result)
        recognized += len(re.findall(r"[\u4e00-\u9fffA-Za-z0-9]", text))
        chunks.append(f"--- 第 {page_number} 页 ---\n{text}")
        print(f"[{pdf_path.stem}] {page_number}/{page_count} 页，累计可读字符 {recognized}", flush=True)
    output_path.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")
    return {"pages": page_count, "recognized_characters": recognized, "output": str(output_path)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", action="append", help="只处理指定案例；可重复")
    parser.add_argument("--force", action="store_true", help="覆盖已有 OCR 文本")
    parser.add_argument("--dpi", type=int, default=170)
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    selected = set(args.case_id or [])
    records = [r for r in manifest["records"] if r["text_quality"] == "ocr-required" and (not selected or r["case_id"] in selected)]
    if not records:
        print("没有待 OCR 的案例。")
        return 0
    results = []
    for record in records:
        pdf_path = ROOT / record["local_raw_paper"]
        output_path = DATA_ROOT / "ocr" / record["case_id"] / "paper.txt"
        if output_path.exists() and not args.force:
            print(f"跳过已有文件：{record['case_id']}")
            continue
        results.append({"case_id": record["case_id"], **ocr_pdf(pdf_path, output_path, args.dpi)})
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

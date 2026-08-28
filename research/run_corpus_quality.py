"""Run local-only pipeline checks over the unlabeled research corpus."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from modelscore.corpus import QUALITY_PATH, run_corpus_quality


if __name__ == "__main__":
    report = run_corpus_quality()
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"Report: {QUALITY_PATH}")

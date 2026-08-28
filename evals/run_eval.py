"""离线批量评测；输入为教师标注 JSONL。"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from modelscore.engine import run_review
from modelscore.parser import parse_material


def _mean(values):
    return round(statistics.mean(values), 4) if values else None


def evaluate(annotation_path: Path) -> dict:
    cases = [json.loads(line) for line in annotation_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    outcomes, errors, skipped = [], [], []
    for case in cases:
        if case.get("teacher_annotation_status") == "unlabeled":
            skipped.append({"case_id": case.get("case_id"), "reason": "teacher annotation is incomplete"})
            continue
        started = time.perf_counter()
        try:
            paper = parse_material((annotation_path.parent / case["paper"]).resolve(), "paper")
            problem = parse_material((annotation_path.parent / case["problem"]).resolve(), "problem")
            code_path = (annotation_path.parent / case["code"]).resolve() if case.get("code") else None
            code = parse_material(code_path, "code") if code_path else None
            report = run_review({
                "contest": "国赛 (CUMCM)", "problem": case.get("problem_id", "B"),
                "group": case.get("group", "本科生组"), "region": case.get("region", "未知赛区"), "mode": "during",
            }, problem, paper, code)
            predicted = {d["name"]: d["score"] for d in report["dimensions"]}
            teacher = {k: v for k, v in case.get("teacher_dimensions", {}).items() if isinstance(v, (int, float))}
            dimension_errors = {name: abs(predicted[name] - score) for name, score in teacher.items() if name in predicted}
            actual_risks = set(case.get("teacher_high_risk_rule_ids", []))
            predicted_risks = {r["rule_id"] for r in report["risks"] if r["severity"] == "high"}
            tp = len(actual_risks & predicted_risks)
            outcomes.append({
                "case_id": case["case_id"], "score": report["score"], "provider": report["provider"],
                "parse_ok": bool(paper.text), "dimension_absolute_errors": dimension_errors,
                "tp": tp, "fp": len(predicted_risks - actual_risks), "fn": len(actual_risks - predicted_risks),
                "citations": sum(bool(c.get("evidence")) for c in report["checks"]),
                "accepted_model_citations": (report.get("model_usage") or {}).get("accepted_citations", 0),
                "tokens": (report.get("model_usage") or {}).get("total_tokens", 0),
                "elapsed_ms": round((time.perf_counter() - started) * 1000), "warnings": report["warnings"],
            })
        except Exception as exc:
            errors.append({"case_id": case.get("case_id"), "error": str(exc)})
    tp, fp, fn = (sum(o[key] for o in outcomes) for key in ("tp", "fp", "fn"))
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = 2 * precision * recall / (precision + recall) if precision is not None and recall is not None and precision + recall else None
    all_dimension_errors = [value for o in outcomes for value in o["dimension_absolute_errors"].values()]
    return {
        "cases": len(cases), "completed": len(outcomes), "skipped": skipped, "errors": errors,
        "metrics": {
            "parse_success_rate": round(sum(o["parse_ok"] for o in outcomes) / len(outcomes), 4) if outcomes else None,
            "dimension_mae": _mean(all_dimension_errors), "high_risk_precision": precision,
            "high_risk_recall": recall, "high_risk_f1": f1, "mean_elapsed_ms": _mean([o["elapsed_ms"] for o in outcomes]),
            "mean_total_tokens": _mean([o["tokens"] for o in outcomes]),
        },
        "outcomes": outcomes,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("annotations", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "eval-results.json")
    args = parser.parse_args()
    result = evaluate(args.annotations.resolve())
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result["metrics"], ensure_ascii=False, indent=2))
    if result["errors"]:
        raise SystemExit(1)

import json
import tempfile
import unittest
from pathlib import Path

from evals.run_eval import evaluate


class EvalSafetyTest(unittest.TestCase):
    def test_unlabeled_cases_are_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            annotations = Path(tmp) / "annotations.jsonl"
            annotations.write_text(json.dumps({
                "case_id": "unlabeled-001",
                "teacher_annotation_status": "unlabeled",
                "paper": "missing-paper.pdf",
                "problem": "missing-problem.pdf",
                "teacher_dimensions": {"假设合理性": None},
                "teacher_high_risk_rule_ids": [],
            }, ensure_ascii=False) + "\n", encoding="utf-8")
            result = evaluate(annotations)
            self.assertEqual(result["cases"], 1)
            self.assertEqual(result["completed"], 0)
            self.assertEqual(len(result["skipped"]), 1)
            self.assertIsNone(result["metrics"]["dimension_mae"])
            self.assertIsNone(result["metrics"]["high_risk_f1"])


if __name__ == "__main__":
    unittest.main()

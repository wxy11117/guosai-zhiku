import json
import tempfile
import unittest
from pathlib import Path

import modelscore.corpus as corpus


class CorpusGovernanceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        data = root / "data"
        text_path = data / "anonymized" / "case-a" / "paper.txt"
        text_path.parent.mkdir(parents=True)
        text_path.write_text("摘要\n参赛学校：测试大学\n联系邮箱：name@example.com\n模型建立与结果分析", encoding="utf-8")
        problem = data / "raw" / "case-a" / "problem.txt"
        problem.parent.mkdir(parents=True)
        problem.write_text("CUMCM A题", encoding="utf-8")
        manifest = root / "manifest.json"
        manifest.write_text(json.dumps({"records": [{
            "case_id": "case-a", "year": 2024, "problem_id": "A", "text_quality": "usable",
            "local_anonymized_text": str(text_path.relative_to(root)).replace("\\", "/"),
            "local_problem": str(problem.relative_to(root)).replace("\\", "/"),
        }]}), encoding="utf-8")
        self.old = (corpus.ROOT, corpus.DATA_ROOT, corpus.MANIFEST_PATH, corpus.REVIEWS_PATH, corpus.REVIEWED_ROOT)
        corpus.ROOT = root
        corpus.DATA_ROOT = data
        corpus.MANIFEST_PATH = manifest
        corpus.REVIEWS_PATH = data / "reviews.json"
        corpus.REVIEWED_ROOT = data / "reviewed"

    def tearDown(self):
        corpus.ROOT, corpus.DATA_ROOT, corpus.MANIFEST_PATH, corpus.REVIEWS_PATH, corpus.REVIEWED_ROOT = self.old
        self.tmp.cleanup()

    def test_scan_and_review_gate(self):
        detail = corpus.case_detail("case-a")
        self.assertFalse(detail["model_upload_allowed"])
        self.assertEqual({f["kind"] for f in detail["pii_findings"]}, {"email", "school_or_author"})
        actions = {f["id"]: "redact" for f in detail["pii_findings"]}
        approved = corpus.update_review("case-a", {"status": "approved", "actions": actions, "notes": "checked"})
        self.assertTrue(approved["model_upload_allowed"])
        reviewed = (corpus.REVIEWED_ROOT / "case-a" / "paper.txt").read_text(encoding="utf-8")
        self.assertNotIn("测试大学", reviewed)
        self.assertNotIn("name@example.com", reviewed)

    def test_cannot_approve_unresolved_finding(self):
        with self.assertRaisesRegex(ValueError, "未处理"):
            corpus.update_review("case-a", {"status": "approved", "actions": {}})


if __name__ == "__main__":
    unittest.main()

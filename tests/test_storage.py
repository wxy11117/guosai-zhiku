import tempfile
import unittest
from pathlib import Path

import modelscore.storage as storage


class StorageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old_path = storage.DB_PATH
        storage.DB_PATH = Path(self.tmp.name) / "modelscore.sqlite3"

    def tearDown(self):
        storage.DB_PATH = self.old_path
        self.tmp.cleanup()

    def test_workflow_sync_persists_order_and_deletion(self):
        first = {"id": "WF-FIRST", "title": "第一项", "status": "已完成"}
        second = {"id": "WF-SECOND", "title": "第二项", "status": "失败"}
        storage.sync_workflows([first, second])
        self.assertEqual([item["id"] for item in storage.list_workflows()], ["WF-FIRST", "WF-SECOND"])
        storage.sync_workflows([second])
        self.assertEqual(storage.list_workflows(), [second])

    def test_job_state_survives_and_running_job_is_recovered(self):
        storage.save_job("JOB-ABC123", {"status": "reviewing", "progress": 55})
        self.assertEqual(storage.get_job("JOB-ABC123")["progress"], 55)
        storage.init_db(recover_jobs=True)
        recovered = storage.get_job("JOB-ABC123")
        self.assertEqual(recovered["status"], "failed")
        self.assertIn("重启", recovered["error"])

    def test_rejects_oversized_or_invalid_workflow_list(self):
        with self.assertRaises(ValueError):
            storage.sync_workflows([{"id": "bad id", "title": "x"}])
        with self.assertRaises(ValueError):
            storage.sync_workflows("not-a-list")


if __name__ == "__main__":
    unittest.main()

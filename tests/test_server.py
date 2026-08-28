import tempfile
import unittest
import json
import urllib.error
import urllib.request
import threading
from pathlib import Path
from http.server import ThreadingHTTPServer

import server
import modelscore.storage as storage


class ServerTest(unittest.TestCase):
    def test_allowed_formats_match_frontend_contract(self):
        self.assertEqual(server.ALLOWED["paper"], {".pdf", ".docx", ".txt"})
        self.assertNotIn(".rar", server.ALLOWED["code"])

    def test_execute_creates_downloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            problem = root / "problem.txt"
            paper = root / "paper.txt"
            code = root / "main.py"
            problem.write_text("国赛 B 题问题一问题二", encoding="utf-8")
            paper.write_text("摘要 模型假设 目标函数 约束条件 结果表明 结论 参考文献", encoding="utf-8")
            code.write_text("random_seed=42", encoding="utf-8")
            old = server.TASKS
            server.TASKS = root / "tasks"
            try:
                report = server._execute(
                    {"contest": "CUMCM", "problem": "B", "group": "本科生组", "region": "江苏赛区", "mode": "during"},
                    {"problem": problem, "paper": paper, "code": code},
                )
                report_dir = server.TASKS / report["report_id"]
                self.assertTrue((report_dir / "report.json").exists())
                self.assertTrue((report_dir / "report.pdf").exists())
            finally:
                server.TASKS = old

    def test_local_data_files_are_not_statically_served(self):
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{httpd.server_port}/data/modelscore.sqlite3"
            with self.assertRaises(urllib.error.HTTPError) as caught:
                urllib.request.urlopen(url, timeout=3)
            self.assertEqual(caught.exception.code, 403)
        finally:
            httpd.shutdown()
            httpd.server_close()

    def test_workflow_http_api_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            old_db = storage.DB_PATH
            storage.DB_PATH = Path(tmp) / "api.sqlite3"
            httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
            thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            thread.start()
            try:
                base = f"http://127.0.0.1:{httpd.server_port}"
                body = json.dumps({"workflows": [{"id": "WF-API", "title": "API 自检"}]}).encode("utf-8")
                request = urllib.request.Request(
                    base + "/api/workflows/sync", data=body,
                    headers={"Content-Type": "application/json"}, method="POST",
                )
                with urllib.request.urlopen(request, timeout=3) as response:
                    self.assertEqual(json.load(response)["count"], 1)
                with urllib.request.urlopen(base + "/api/workflows", timeout=3) as response:
                    self.assertEqual(json.load(response)["workflows"][0]["id"], "WF-API")
            finally:
                httpd.shutdown()
                httpd.server_close()
                storage.DB_PATH = old_db


if __name__ == "__main__":
    unittest.main()

import tempfile
import unittest
import zipfile
from pathlib import Path

from modelscore.engine import run_review
from modelscore.parser import analyze_structure, parse_material
from modelscore.rules import RULES, load_rules
from modelscore.reporting import save_pdf


PAPER = """摘要
本文针对问题一和问题二建立优化模型。首先给出模型假设和变量说明，并根据题意建立目标函数与约束条件。
模型建立
技术路线如下，本文提出改进算法，算法步骤通过迭代完成。各子问题的输入输出关系明确。
结果分析
结果表明核心指标提高 12%。我们进行了敏感性分析、误差分析、稳健性检验和对比实验，并解释异常情况。
如图 1 和表 1 所示，横坐标单位为小时，纵坐标单位为百分比。数据来源见注释。
模型评价
模型优点是可解释，缺点与局限性是对极端情况刻画不足，后续可以放宽假设。
参考文献
[1] 示例文献，出版社，2025。
"""


class EngineTest(unittest.TestCase):
    def test_rule_count(self):
        self.assertEqual(len(RULES), 42)
        rules, config = load_rules()
        self.assertEqual(len(rules), 42)
        self.assertAlmostEqual(sum(config["dimension_weights"].values()), 1.0)

    def test_end_to_end_local_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            problem_path = root / "problem.txt"
            paper_path = root / "paper.txt"
            code_path = root / "code.zip"
            problem_path.write_text("全国大学生数学建模竞赛 B 题，完成问题一和问题二。", encoding="utf-8")
            paper_path.write_text(PAPER, encoding="utf-8")
            with zipfile.ZipFile(code_path, "w") as archive:
                archive.writestr("main.py", "import random\nrandom.seed(42)\nprint('ok')")
                archive.writestr("requirements.txt", "numpy==2.0")
                archive.writestr("data/input.csv", "x,y\n1,2")
                archive.writestr("results/figure.png", b"png")
                archive.writestr("README.md", "运行 main.py 生成 figure 和 table")
            report = run_review(
                {"contest": "国赛 (CUMCM)", "problem": "B", "group": "本科生组", "region": "江苏赛区", "mode": "during"},
                parse_material(problem_path, "problem"), parse_material(paper_path, "paper"), parse_material(code_path, "code"),
            )
            self.assertEqual(len(report["checks"]), 42)
            self.assertEqual(len(report["dimensions"]), 6)
            self.assertGreaterEqual(report["score"], 45)
            self.assertEqual(report["provider"], "local-rules")
            self.assertTrue(report["report_id"].startswith("MYC-"))
            self.assertEqual(report["rule_version"], "cumcm-v1.0.0")
            self.assertIn("section_count", report["parsing"]["paper"])
            pdf_path = root / "report.pdf"
            save_pdf(report, pdf_path)
            self.assertGreater(pdf_path.stat().st_size, 1000)

    def test_structure_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "paper.txt"
            path.write_text("摘要\n模型假设\n敏感性分析\n图 1\n表 1\n参考文献", encoding="utf-8")
            metadata = analyze_structure(parse_material(path, "paper"))
            self.assertGreaterEqual(metadata["section_count"], 4)
            self.assertEqual(metadata["figure_mentions"], 1)
            self.assertEqual(metadata["table_mentions"], 1)


if __name__ == "__main__":
    unittest.main()

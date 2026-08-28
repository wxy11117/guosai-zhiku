"""JSON 与中文 PDF 报告产物。"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


FONT_CANDIDATES = [
    Path("C:/Windows/Fonts/msyh.ttc"), Path("C:/Windows/Fonts/simhei.ttf"), Path("C:/Windows/Fonts/simsun.ttc")
]


def save_json(report: dict, path: Path) -> None:
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def _font() -> str:
    for path in FONT_CANDIDATES:
        if path.exists():
            try:
                pdfmetrics.registerFont(TTFont("ModelScoreCN", str(path), subfontIndex=0))
                return "ModelScoreCN"
            except Exception:
                continue
    return "Helvetica"


def save_pdf(report: dict, path: Path) -> None:
    font = _font()
    styles = getSampleStyleSheet()
    title = ParagraphStyle("CNTitle", parent=styles["Title"], fontName=font, fontSize=20, leading=28, alignment=TA_CENTER)
    h2 = ParagraphStyle("CNH2", parent=styles["Heading2"], fontName=font, fontSize=13, leading=20, textColor=colors.HexColor("#16325c"), spaceBefore=8)
    body = ParagraphStyle("CNBody", parent=styles["BodyText"], fontName=font, fontSize=9.5, leading=15)
    small = ParagraphStyle("CNSmall", parent=body, fontSize=8, leading=12, textColor=colors.HexColor("#52606d"))
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=17 * mm, rightMargin=17 * mm, topMargin=16 * mm, bottomMargin=16 * mm)
    story = [
        Paragraph("模评云 CUMCM 赛中诊断报告", title),
        Spacer(1, 4 * mm),
        Paragraph(f"报告编号：{escape(report['report_id'])}　生成时间：{escape(report['generated_at'])}", small),
        Spacer(1, 3 * mm),
        Paragraph(escape(report["summary"]), body),
        Spacer(1, 4 * mm),
    ]
    meta = report["task"]
    overview = [
        ["竞赛", meta.get("contest", "CUMCM"), "题号", meta.get("problem", "")],
        ["组别", meta.get("group", ""), "赛区", meta.get("region", "")],
        ["综合健康度", str(report["score"]), "总体置信度", f"{report['confidence']:.0%}"],
        ["评审来源", report["provider"], "模型", report.get("model") or "未调用"],
    ]
    table = Table(overview, colWidths=[28 * mm, 57 * mm, 28 * mm, 57 * mm])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), font), ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef4ff")),
        ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#eef4ff")),
        ("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [table, Paragraph("六维评分", h2)]
    dim_rows = [["维度", "分数", "通过项", "置信度"]] + [[d["name"], d["score"], f"{d['passed']}/{d['total']}", f"{d['confidence']:.0%}"] for d in report["dimensions"]]
    dim_table = Table(dim_rows, colWidths=[66 * mm, 30 * mm, 32 * mm, 32 * mm])
    dim_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), font), ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16325c")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#cbd5e1")), ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))
    story += [dim_table, Paragraph("优先风险与修改建议", h2)]
    for index, item in enumerate(report["risks"], 1):
        evidence = item.get("evidence") or {}
        source = f"{evidence.get('file', '未定位')} 第 {evidence.get('page', '?')} 页"
        quote = evidence.get("quote") or "未定位到原文证据，需人工复核。"
        story += [
            Paragraph(f"{index}. [{escape(item['severity'].upper())}] {escape(item['title'])}（{escape(item['rule_id'])}）", h2),
            Paragraph(f"原因：{escape(item['reason'])}<br/>建议：{escape(item['action'])}<br/>证据：{escape(source)} — {escape(quote)}", body),
        ]
    story += [PageBreak(), Paragraph("42 项规则检查明细", h2)]
    for item in report["checks"]:
        status = "通过" if item["passed"] else "需改进"
        story.append(Paragraph(f"{escape(item['rule_id'])}　{escape(item['title'])}　[{status}]", body))
    if report.get("warnings"):
        story += [Paragraph("运行提示", h2)] + [Paragraph(escape(w), small) for w in report["warnings"]]
    parsing = report.get("parsing", {}).get("paper", {})
    story += [
        Paragraph("解析与审计信息", h2),
        Paragraph(escape(
            f"规则版本：{report.get('rule_version', '未知')}；页码定位：{parsing.get('page_locator', '未知')}；"
            f"字符数：{parsing.get('char_count', 0)}；章节：{parsing.get('section_count', 0)}；"
            f"公式提及：{parsing.get('formula_mentions', 0)}；图：{parsing.get('figure_mentions', 0)}；表：{parsing.get('table_mentions', 0)}。"
        ), body),
    ]
    if report.get("model_usage"):
        usage = report["model_usage"]
        story.append(Paragraph(escape(
            f"模型用量：输入 {usage.get('input_tokens', 0)} tokens，输出 {usage.get('output_tokens', 0)} tokens，"
            f"耗时 {usage.get('latency_ms', 0)} ms，通过服务端引文校验 {usage.get('accepted_citations', 0)} 条。"
        ), body))
    story.append(Paragraph("免责声明：本报告仅用于赛前自查与教学交流，不代表竞赛官方评审结果。", small))
    doc.build(story)

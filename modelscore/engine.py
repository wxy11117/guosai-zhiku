"""规则优先、证据可追踪的 CUMCM 诊断引擎。"""

from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone

from .parser import ParsedMaterial, analyze_structure, find_evidence
from .rules import load_rules


DIMENSIONS = ["假设合理性", "建模创新性", "结果正确性", "表述清晰性", "代码可复现性", "图文美观性"]


def _derived_tokens(paper: ParsedMaterial, code: ParsedMaterial | None) -> dict[str, bool]:
    text = paper.text
    return {
        "__CODE_PRESENT__": bool(code and (code.text or code.inventory)),
        "__FIGURE_PRESENT__": bool(text and ("图" in text or "figure" in text.lower())),
        "__ANONYMITY_OK__": not any(word in text[:5000] for word in ["学校：", "学院：", "指导教师", "作者："]),
    }


def _rule_check(rule, paper, code, tokens):
    if len(rule.keywords) == 1 and rule.keywords[0].startswith("__"):
        passed = tokens.get(rule.keywords[0], False)
        evidence = {"file": paper.name, "page": 1, "quote": "自动结构检查：条件满足。"} if passed else None
    else:
        target = code if rule.dimension == "代码可复现性" and code else paper
        evidence = find_evidence(target, rule.keywords)
        if not evidence and target is not paper:
            evidence = find_evidence(paper, rule.keywords)
        passed = evidence is not None
    return passed, evidence


def _local_report(task: dict, problem: ParsedMaterial, paper: ParsedMaterial, code: ParsedMaterial | None) -> dict:
    rules, rule_config = load_rules()
    tokens = _derived_tokens(paper, code)
    results = []
    penalties = defaultdict(float)
    passed_by_dimension = defaultdict(int)
    for rule in rules:
        passed, evidence = _rule_check(rule, paper, code, tokens)
        if passed:
            passed_by_dimension[rule.dimension] += 1
        else:
            penalties[rule.dimension] += rule.penalty
        results.append({
            "rule_id": rule.id,
            "dimension": rule.dimension,
            "title": rule.title,
            "passed": passed,
            "severity": "info" if passed else rule.severity,
            "score_delta": 0 if passed else -rule.penalty,
            "confidence": 0.82 if passed else 0.68,
            "evidence": evidence,
            "reason": "已找到可核验内容。" if passed else "在可解析材料中未找到满足该检查项的明确证据。",
            "action": "保持该部分与全文结论一致。" if passed else rule.recommendation,
            "source": "local-rule",
        })

    dimensions = []
    for name in DIMENSIONS:
        score = max(float(rule_config.get("minimum_score", 45.0)), round(100 - penalties[name], 1))
        dimensions.append({
            "name": name,
            "score": score,
            "confidence": round(0.55 + passed_by_dimension[name] / 7 * 0.35, 2),
            "passed": passed_by_dimension[name],
            "total": 7,
        })
    weights = rule_config.get("dimension_weights", {})
    weight_sum = sum(float(weights.get(item["name"], 0)) for item in dimensions)
    total_score = round(
        sum(item["score"] * float(weights.get(item["name"], 1 / len(dimensions))) for item in dimensions) / (weight_sum or 1), 1
    )
    risks = [item for item in results if not item["passed"]]
    risks.sort(key=lambda item: ({"high": 0, "medium": 1, "low": 2}.get(item["severity"], 3), item["score_delta"]))
    warnings = problem.warnings + paper.warnings + (code.warnings if code else [])
    return {
        "schema_version": "1.0",
        "engine_version": "0.3.0",
        "rule_version": rule_config.get("version", "cumcm-v1"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task": task,
        "score": total_score,
        "confidence": round(sum(d["confidence"] for d in dimensions) / len(dimensions), 2),
        "dimensions": dimensions,
        "checks": results,
        "risks": risks[:12],
        "summary": f"完成 42 项 CUMCM 规则检查，综合健康度 {total_score}。建议优先处理高风险且缺少原文证据的检查项。",
        "warnings": warnings,
        "parsing": {
            "problem": analyze_structure(problem), "paper": analyze_structure(paper),
            "code": analyze_structure(code) if code else None,
        },
        "provider": "local-rules",
        "model": None,
        "model_usage": None,
    }


def _extract_output_text(response: dict) -> str:
    if response.get("output_text"):
        return response["output_text"]
    for item in response.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                return content["text"]
    raise ValueError("OpenAI 响应中没有文本输出")


def _openai_review(local: dict, paper: ParsedMaterial) -> dict | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
    candidates = [c for c in local["checks"] if not c["passed"]][:14]
    input_payload = {
        "task": local["task"],
        "local_score": local["score"],
        "candidate_gaps": candidates,
        "paper_excerpt": paper.text[:45_000],
    }
    schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "rule_id": {"type": "string"}, "severity": {"type": "string", "enum": ["high", "medium", "low"]},
                        "reason": {"type": "string"}, "action": {"type": "string"}, "quote": {"type": "string"}, "page": {"type": "integer"},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    },
                    "required": ["rule_id", "severity", "reason", "action", "quote", "page", "confidence"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["summary", "findings"], "additionalProperties": False,
    }
    prompt = (
        "你是严格的全国大学生数学建模竞赛论文评审助手。只能依据输入论文摘录和候选规则缺口复核，"
        "不得代写论文，不得虚构页码或引文。找不到明确证据时不要输出该 finding。"
        "输出最多 8 条最重要且可操作的发现，quote 必须逐字来自 paper_excerpt。\n\n" +
        json.dumps(input_payload, ensure_ascii=False)
    )
    payload = {
        "model": model,
        "input": prompt,
        "reasoning": {"effort": os.getenv("OPENAI_REASONING_EFFORT", "low")},
        "store": False,
        "safety_identifier": hashlib.sha256(
            (local["task"].get("region", "unknown") + "|modelscore-local-user").encode("utf-8")
        ).hexdigest()[:32],
        "text": {"format": {"type": "json_schema", "name": "cumcm_review", "strict": True, "schema": schema}},
    }
    request = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=120) as response:
        body = json.loads(response.read().decode("utf-8"))
    result = json.loads(_extract_output_text(body))
    result["model"] = model
    usage = body.get("usage", {})
    result["usage"] = {
        "input_tokens": usage.get("input_tokens", 0), "output_tokens": usage.get("output_tokens", 0),
        "total_tokens": usage.get("total_tokens", 0), "latency_ms": round((time.perf_counter() - started) * 1000),
        "response_id": body.get("id"),
    }
    return result


def run_review(task: dict, problem: ParsedMaterial, paper: ParsedMaterial, code: ParsedMaterial | None) -> dict:
    report = _local_report(task, problem, paper, code)
    try:
        enhancement = _openai_review(report, paper)
        if enhancement:
            checks = {item["rule_id"]: item for item in report["checks"]}
            for finding in enhancement.get("findings", []):
                target = checks.get(finding["rule_id"])
                quote = finding.get("quote", "")
                if not target or not quote or quote not in paper.text:
                    continue
                evidence = find_evidence(paper, (quote,))
                if not evidence:
                    continue
                target.update({
                    "severity": finding["severity"], "reason": finding["reason"], "action": finding["action"],
                    "confidence": finding["confidence"],
                    "evidence": evidence, "source": "openai-review",
                })
            accepted = sum(1 for check in report["checks"] if check["source"] == "openai-review")
            report["summary"] = enhancement.get("summary") or report["summary"]
            report["provider"] = "local-rules+openai"
            report["model"] = enhancement["model"]
            report["model_usage"] = {**enhancement.get("usage", {}), "accepted_citations": accepted, "citation_validation": "exact-substring+server-page"}
            report["risks"] = sorted(
                [c for c in report["checks"] if not c["passed"]],
                key=lambda item: ({"high": 0, "medium": 1, "low": 2}.get(item["severity"], 3), item["score_delta"]),
            )[:12]
    except urllib.error.HTTPError as exc:
        reason = {401: "API Key 无效或已失效", 403: "项目无权调用所选模型", 429: "额度或速率限制"}.get(exc.code, f"HTTP {exc.code}")
        report["warnings"].append(f"ChatGPT 增强评审不可用（{reason}），已保留本地规则结果。")
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        report["warnings"].append(f"ChatGPT 增强评审不可用，已保留本地规则结果：{type(exc).__name__}")
    report["report_id"] = "MYC-" + hashlib.sha256(
        (paper.name + report["generated_at"]).encode("utf-8")
    ).hexdigest()[:12].upper()
    return report

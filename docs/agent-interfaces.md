# ModelScoreAgent 接口契约 v0.1

本文定义智能体的输入、输出和中间数据结构。实现时应优先保持这些字段稳定。

## ReviewTask

```json
{
  "id": "review_20260531_0001",
  "contest": "MathorCup",
  "problem": "B",
  "teamId": "BMC2602161",
  "mode": "赛前冲奖",
  "phase": "during_contest",
  "region": "江苏赛区",
  "files": [
    {
      "name": "BMC2602161.pdf",
      "type": "paper",
      "mimeType": "application/pdf",
      "size": 2048000
    },
    {
      "name": "problem-statement.pdf",
      "type": "reference",
      "mimeType": "application/pdf",
      "size": 512000
    }
  ],
  "options": {
    "checkFormat": true,
    "checkCode": true,
    "estimateAward": true,
    "teacherReport": false,
    "useLargeModel": true
  },
  "createdAt": "2026-05-31T16:00:00.000Z"
}
```

## ParsedPaper

```json
{
  "language": "zh-CN",
  "pageCount": 29,
  "sections": [
    { "name": "摘要", "found": true, "page": 1 },
    { "name": "问题重述", "found": true, "page": 3 },
    { "name": "模型假设", "found": true, "page": 5 },
    { "name": "参考文献", "found": true, "page": 27 }
  ],
  "figures": { "count": 12, "referencedCount": 10 },
  "tables": { "count": 8, "referencedCount": 8 },
  "formulas": { "count": 34, "numberedCount": 31 },
  "references": { "count": 16, "formatIssues": 2 },
  "attachments": {
    "hasCode": true,
    "hasData": true,
    "hasRunInstructions": false
  },
  "warnings": [
    "部分图未在正文中引用",
    "代码附件缺少运行说明"
  ]
}
```

## ModelReasoning

```json
{
  "phase": "during_contest",
  "modelRationality": {
    "score": 84,
    "summary": "模型假设基本合理，但缺少部分边界条件解释。",
    "evidence": [
      "目标函数与题目核心目标一致",
      "约束条件覆盖主要物理限制",
      "未充分说明极端场景下的假设有效性"
    ]
  },
  "resultValidity": {
    "score": 82,
    "summary": "结果趋势合理，但敏感性分析不足。",
    "evidence": [
      "关键结果与模型目标方向一致",
      "缺少参数扰动后的稳定性验证"
    ]
  },
  "revisionAdvice": [
    "补充关键参数的敏感性分析",
    "解释异常值和边界场景下的模型表现"
  ]
}
```

## RubricProfile

```json
{
  "id": "rubric_mathorcup_default",
  "contest": "MathorCup",
  "problem": "B",
  "version": "2026.1",
  "dimensions": [
    { "key": "assumption", "name": "假设合理性", "weight": 18 },
    { "key": "innovation", "name": "建模创新性", "weight": 16 },
    { "key": "result", "name": "结果正确性", "weight": 22 },
    { "key": "clarity", "name": "表述清晰性", "weight": 16 },
    { "key": "reproducibility", "name": "代码可复现性", "weight": 14 },
    { "key": "visual", "name": "图文美观性", "weight": 14 }
  ],
  "formatRules": [
    "论文题号与报名题号一致",
    "首页包含题目、摘要和关键词",
    "正文引用按方括号编号",
    "附录提供软件名称、运行命令和源程序"
  ]
}
```

## DimensionScore

```json
{
  "key": "reproducibility",
  "name": "代码可复现性",
  "score": 76,
  "weight": 14,
  "confidence": 0.82,
  "evidence": [
    "检测到代码附件",
    "检测到数据文件",
    "未检测到完整运行命令"
  ],
  "deductions": [
    {
      "code": "missing_run_instructions",
      "title": "缺少运行说明",
      "points": 8,
      "reason": "附件中没有明确入口脚本、依赖版本和数据路径。"
    }
  ]
}
```

## RiskItem

```json
{
  "id": "risk_001",
  "priority": "high",
  "dimension": "reproducibility",
  "title": "完善代码复现说明",
  "reason": "代码附件存在，但缺少运行命令和依赖说明，会影响评委复现实验。",
  "action": "在附录中补充 Python/Matlab 版本、依赖安装命令、入口脚本、数据路径和输出文件说明。",
  "relatedRule": "附录提供软件名称、运行命令和源程序"
}
```

## AwardEstimate

```json
{
  "contest": "CUMCM",
  "region": "江苏赛区",
  "levels": [
    { "label": "国赛一等奖", "probability": 8 },
    { "label": "国赛二等奖", "probability": 31 },
    { "label": "江苏赛区一等奖", "probability": 44 },
    { "label": "江苏赛区二等奖", "probability": 15 }
  ],
  "summary": "当前处于一等奖冲刺区间，但代码复现和敏感性分析仍是主要风险。",
  "explanations": [
    "模型结构完整，符合该赛事对建模过程的要求。",
    "结果展示接近往年一等奖论文特征。",
    "代码复现说明不足，降低了高奖项置信度。"
  ],
  "referenceSignals": [
    "比赛评价标准",
    "往年获奖作品特点",
    "论文六维评分",
    "代码与附件完整性"
  ]
}
```

不同比赛必须使用对应奖项体系。例如：

- 美赛：`O 奖`、`F 奖`、`S 奖`、`M 奖`
- 国赛：`国赛一等奖`、`国赛二等奖`、`赛区一等奖`、`赛区二等奖`
- 常规中文赛事：按赛事规则配置，例如 `一等奖`、`二等奖`、`三等奖`、`优秀奖` 或 `成功参赛奖`

如果奖项体系依赖地区或赛区，创建任务时必须收集 `region`。

## ReviewReport

```json
{
  "id": "report_20260531_0001",
  "taskId": "review_20260531_0001",
  "status": "completed",
  "generatedAt": "2026-05-31T16:10:00.000Z",
  "summary": {
    "totalScore": 83.5,
    "grade": "一等奖冲刺区间",
    "confidence": 0.84,
    "highRiskCount": 3
  },
  "dimensions": [],
  "modelReasoning": {},
  "risks": [],
  "awardEstimate": {},
  "parserWarnings": [],
  "nextActions": [
    "补充敏感性分析与误差解释",
    "完善代码运行命令、数据路径和图表生成说明",
    "压缩摘要背景铺垫并前置核心结论"
  ],
  "audit": {
    "rubricId": "rubric_mathorcup_default",
    "agentVersion": "0.1.0",
    "modelProvider": "local-rules",
    "externalUpload": false
  }
}
```

## Agent API 草案

```js
const agent = new ModelScoreAgent({
  rubricStore,
  parser,
  scorer,
  awardEstimator,
});

const task = agent.createReviewTask(input);
const report = await agent.runReview(task);
```

## 错误格式

```json
{
  "status": "failed",
  "code": "unsupported_file_type",
  "message": "当前版本仅支持 PDF、DOCX 和 ZIP。",
  "recoverable": true
}
```

## 与前端工作台的边界

前端只负责：

- 收集任务输入
- 展示智能体状态
- 渲染报告
- 触发导出

前端不负责：

- 计算维度分
- 生成扣分理由
- 估算奖项概率
- 拼接报告结论

这些逻辑全部归属 `ModelScoreAgent` 或其子模块。

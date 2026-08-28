# 模评云技术路线

## 架构建议

- 前端：Web 工作台，后续可迁移到 Vite + React 或 Vue。
- 后端：评分任务 API、文件解析服务、规则引擎、报告导出服务。
- 存储：任务元数据使用关系型数据库，论文和附件使用对象存储或本地文件存储。
- 桌面端：在 Web 工作台稳定后再封装桌面客户端。

## 评分服务拆分

1. `parser-service`：PDF/DOCX 文本提取、章节识别、公式和图表索引。
2. `rubric-service`：赛事规则、权重配置、扣分项和规则版本管理。
3. `scoring-service`：六维评分、风险定位、奖项概率估计。
4. `report-service`：JSON、PDF、Word 报告生成。

## 智能体设计

评分流程由 `ModelScoreAgent` 编排。智能体的职责、状态流转和数据契约见：

- [agent-design.md](agent-design.md)
- [agent-interfaces.md](agent-interfaces.md)

## API 草案

```http
POST /api/reviews
GET /api/reviews/:id
POST /api/reviews/:id/files
POST /api/reviews/:id/run
GET /api/reviews/:id/report
GET /api/rubrics
PUT /api/rubrics/:id
```

## 近期工程任务

1. 把静态工作台拆成模块：任务表单、队列状态、评分矩阵、建议列表、规则编辑器。
2. 定义评分结果 JSON Schema。
3. 实现本地文件解析最小闭环：PDF 文本提取与章节检查。
4. 增加报告导出模板。
5. 引入测试：评分计算单元测试、报告快照测试、浏览器交互测试。

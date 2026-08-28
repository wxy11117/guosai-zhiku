# 国赛智库（模评云）

国赛智库整合 2015—2025 国赛资料、常用建模方法、优秀论文索引与课程学习资源，并通过模评云官网提供独立直达入口。当前仓库同时包含官网、智库页面、下载页和本地服务代码。

## 当前版本

- 官网入口：[index.html](index.html)
- 软件工作台：[app.html](app.html)
- 下载页：[download.html](download.html)
- 智能体设计：[docs/agent-design.md](docs/agent-design.md)
- 当前开发阶段：v0.5.0，CUMCM 真实诊断、SQLite 持久化与本地研究语料治理 MVP

## v0.1 目标

1. 跑通论文评审主流程：选择竞赛、题号、队伍编号、论文文件和评审模式。
2. 展示可解释评分：综合分、六维评分、奖项概率、高风险项和优先修改建议。
3. 支持规则权重调节：先在前端模拟权重变更，为后端规则引擎预留接口。
4. 支持报告导出：当前导出 JSON，后续扩展为 PDF / Word 报告。

## 已实现的真实能力

1. 解析 PDF、DOCX、TXT 论文和赛题。
2. 静态读取 ZIP 代码目录，不执行用户代码。
3. 按 CUMCM 六维 42 项版本化规则生成证据化诊断。
4. 可选调用 OpenAI Responses API 复核高风险项。
5. 异步任务进度、结构化 JSON 和中文 PDF 报告。
6. 教师标注模板与离线批量评测工具。
7. 本地研究语料库管理页、匿名化人工复核门禁、中文 OCR 与未标注流水线质检。
8. 工作流与异步任务状态写入 `data/modelscore.sqlite3`，服务重启后仍可读取已完成任务和报告。

语料库管理入口：`http://127.0.0.1:4186/corpus.html`。原始语料目录被静态服务器拒绝访问；未通过人工匿名化复核的案例不能进入模型上传流程。第三方代码仅做 ZIP 静态清单检查，不在主机执行。

国赛智库入口：`http://127.0.0.1:4186/knowledge.html`。整合 2015—2025 历年赛题、61 个常用模型方法、92 篇优秀论文索引、本地模型选路助手，以及按知识点整理的 18 讲课程资料与智能算法专题下载。

重新采集与本地 OCR：

```powershell
& 'C:\Users\Lenovo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' research\acquire_public_corpus.py
& 'C:\Users\Lenovo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' research\ocr_corpus.py
```

完整路线见 [docs/implementation-plan.md](docs/implementation-plan.md)。

## 本地运行

使用 PowerShell 一键启动（默认后台运行并打开浏览器）：

```powershell
.\start.ps1
```

需要在终端查看实时日志时，可使用 `./start.ps1 -Foreground -NoBrowser`。

然后访问 `http://127.0.0.1:4186/app.html`。

默认只使用本地规则。如果要启用 ChatGPT 增强评审，在启动进程前设置：

```powershell
$env:OPENAI_API_KEY = '你的 API Key'
$env:OPENAI_MODEL = 'gpt-5.6-luna'
.\start.ps1
```

启用后，论文文本摘录会发送到 OpenAI API；API Key 仅由后端环境变量读取，不会进入浏览器或报告。无 Key 或 API 调用失败时，系统自动保留本地规则结果。

模型调用使用 `store: false`，并按官方建议发送隐私保护的稳定 `safety_identifier`；报告记录 Token、延迟和通过服务端校验的引文数。当前环境中的 Key 已被接口返回为无效，必须在 OpenAI 平台生成有效项目 Key 后重启服务。

## 评测

教师标注和批量评测说明见 [evals/README.md](evals/README.md)。规则权重位于 [config/cumcm-rules-v1.json](config/cumcm-rules-v1.json)，修改权重后应先运行评测集。

## 测试

```powershell
& 'C:\Users\Lenovo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m unittest discover -s tests -v
```

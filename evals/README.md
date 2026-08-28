# 教师标注与批量评测

1. 将匿名论文、赛题和代码放在本目录下自建的 `papers/`、`problems/`、`code/` 文件夹。
2. 复制 `annotations.template.jsonl` 为 `annotations.jsonl`，每行填写一个案例。
3. 教师填写六维分数和高风险规则编号，完成后将 `teacher_annotation_status` 改为 `complete`。未完成的记录会被评测脚本跳过，不会生成虚假的 MAE/F1。
4. 运行：

```powershell
& 'C:\Users\Lenovo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' evals\run_eval.py evals\annotations.jsonl
```

脚本输出 `eval-results.json`，包含解析成功率、六维平均绝对误差、高风险项 precision/recall/F1、引文定位率、平均耗时与模型 Token 用量。

不要提交真实论文、教师身份信息或 API Key。

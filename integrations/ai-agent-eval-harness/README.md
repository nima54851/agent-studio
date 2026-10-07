# AI Agent Eval Harness Integration

## n8n 工作流
`n8n-eval-pipeline.json` — 评测自动化管道：

1. **触发**: GitHub Webhook（PR opened/updated）
2. **克隆**: 拉取 Agent 源码
3. **执行**: 调用 `eval_runner.py` 跑评测
4. **评分**: LLM-as-Judge 评估输出质量
5. **对比**: 与 baseline 比对，检测回归
6. **报告**: 生成 Markdown 报告并评论到 PR
7. **告警**: 若有回归，发 Slack/Discord 通知

## 环境变量
| 变量 | 说明 |
|------|------|
| `GITHUB_TOKEN` | GitHub 个人访问令牌 |
| `OPENAI_API_KEY` | OpenAI API Key（评分用） |
| `SLACK_WEBHOOK` | Slack Webhook URL（回归告警） |
| `EVAL_BASELINE_JSON` | Baseline 分数 JSON URL |

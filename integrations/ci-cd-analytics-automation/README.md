# CI/CD Analytics Automation — n8n Workflow

## 功能

- 定时拉取 GitHub Actions runs → 解析耗时数据 → 写 InfluxDB
- Flaky test 检测 → 自动创建 GitHub Issue
- DORA 指标异常 → Slack 告警
- 每周 CI 摘要 → 邮件发送工程团队

## 使用方式

在 n8n 中导入 `cicd-analytics-workflow.json`，配置：
- GitHub PAT（Credential）
- InfluxDB / PostgreSQL（指标存储）
- OpenAI / Claude API Key
- Slack Webhook

## 核心节点

1. **Schedule Trigger** — 每 6 小时运行
2. **GitHub API** — 获取 workflow runs + jobs
3. **Code** — 解析耗时 + Flaky 计算
4. **IF Node** — DORA 异常检测
5. **GitHub API** — 创建 Flaky test Issue
6. **AI Agent** — 生成优化建议摘要
7. **Slack** — 发送摘要报告

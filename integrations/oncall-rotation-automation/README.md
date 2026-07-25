# On-Call Rotation Automation — n8n Workflow

## 功能

- PagerDuty Incident Webhook → AI 初步诊断 + Runbook 推送
- 升级超时自动触发 → 升级到下一级
- 定时（交接时） → 生成 AI 摘要报告 → 发送 Slack/Email
- 每周排班自动生成 → Google Calendar 同步 + Slack 公告

## 使用方式

在 n8n 中导入 `oncall-workflow.json`，配置：
- PagerDuty API Key
- Google Calendar API（OAuth2）
- OpenAI / Claude API Key
- Slack Webhook

## 核心节点

1. **PagerDuty Trigger** — 告警事件监听
2. **AI Agent** — 生成初步诊断 + Runbook 链接
3. **Wait** — 超时等待（升级链路）
4. **Google Calendar** — 排班写入
5. **Slack Message** — 交接摘要推送

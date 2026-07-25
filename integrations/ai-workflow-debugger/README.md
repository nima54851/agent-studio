# AI Workflow Debugger — n8n Workflow

## 功能

- n8n execution webhook → 提取失败节点 + 耗时
- AI 根因分析 → 修复建议
- 自动 patch 节点配置（或发 PR）
- Slack 通知 + 执行记录归档

## 使用方式

在 n8n 中导入 `ai-workflow-debugger-workflow.json`，配置：
- n8n API URL + API Key
- OpenAI / Claude API Key
- Slack Webhook

## 核心节点

1. **Webhook** — 接收 n8n 执行失败通知
2. **HTTP Request** — 获取完整执行记录
3. **Code** — 解析节点链 + 提取关键指标
4. **AI Agent** — 根因分析 + 修复建议
5. **Slack Message** — 发送诊断报告

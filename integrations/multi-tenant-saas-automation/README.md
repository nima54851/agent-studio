# Multi-Tenant SaaS Automation — n8n Workflow

## 功能

- Stripe Webhook → 订阅状态同步（激活/暂停/取消）
- 用量上报 → Stripe Metered Billing → 自动开票
- 新租户注册 → 创建 DB Schema → 发欢迎邮件
- 流失风险租户 → 挽留 Offer 自动发送

## 使用方式

在 n8n 中导入 `multi-tenant-workflow.json`，配置：
- Stripe API Key（Credential）
- PostgreSQL 连接（多 Schema 管理）
- SendGrid / SMTP（邮件）
- Slack Webhook

## 核心节点

1. **Stripe Trigger** — 订阅事件监听
2. **PostgreSQL** — 租户 Schema 创建 / 用量写入
3. **AI Agent** — 流失风险评分
4. **Email** — Onboarding / 挽留序列
5. **Slack** — 新租户入驻通知

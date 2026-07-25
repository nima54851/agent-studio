# Contract Review Automation — n8n Workflow

## 功能

- Email/Webhook 接收合同附件（PDF/DOCX/图片）
- 自动路由到 AI 审查节点 → 条款提取 + 风险评分
- 高风险 → Slack 通知法务 + 等待审批
- 低风险 → 自动通过 + 归档 Drive

## 使用方式

在 n8n 中导入 `contract-review-workflow.json`，配置：
- Gmail / IMAP（邮件附件）
- OpenAI / Claude API Key
- Google Drive API（报告归档）
- Slack Webhook

## 核心节点

1. **Email Trigger** — 接收合同附件
2. **Code** — 判断文件类型 + 路由
3. **PDF / DOCX / OCR** — 文件解析
4. **AI Agent** — 条款提取 + 风险评分
5. **IF Node** — 风险分级 → 审批 or 自动通过
6. **Google Drive** — 报告归档

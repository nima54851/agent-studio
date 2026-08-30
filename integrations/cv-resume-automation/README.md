# 📄 CV/Resume Automation — Integration

n8n 工作流集合，用于招聘自动化全链路。

## 📦 包含工作流

| 工作流 | 功能 | 触发方式 |
|--------|------|---------|
| `n8n-cv-parser.json` | 简历上传 → AI 解析 → 人才评分 → 通知 HR | Webhook |
| `n8n-candidate-scorer.json` | 多维度人才评分（技术/经验/文化/综合） | 手动/Schedule |
| `n8n-interview-scheduler.json` | 面试官分配 + Google Calendar 预约 | Webhook |
| `n8n-offer-generator.json` | Offer Letter 模板生成 + 邮件发送 | Manual |

## 导入方法

1. n8n → **Import from File**
2. 选择对应 JSON 文件
3. 配置凭证（OpenAI API Key、Slack Webhook、Google Calendar）
4. Activate

## 快速使用

### 接收简历
```bash
curl -X POST https://your-n8n.com/webhook/cv-upload \
  -F "file=@resume.pdf" \
  -F "job_id=Senior-Engineer-001"
```

### 触发评分
```bash
curl -X POST https://your-n8n.com/webhook/candidate-score \
  -H "Content-Type: application/json" \
  -d '{"resume_json": {...}, "job_description": "..."}'
```

## 环境变量

```
OPENAI_API_KEY=sk-xxx
OPENAI_API_URL=https://api.openai.com/v1
GPT_MODEL=gpt-4o-mini
NOTIFICATION_WEBHOOK=https://hooks.slack.com/xxx
GOOGLE_CALENDAR_ID=primary
```

---
*AI 招聘，从读简历中解放 HR*

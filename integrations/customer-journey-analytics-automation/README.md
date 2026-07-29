# Customer Journey Analytics Automation

## 集成说明

此目录包含客户旅程分析自动化所需的 n8n 工作流配置。

## 文件

- `n8n-journey-analytics.json` — 主工作流：事件接收 → 数据清洗 → 漏斗计算 → AI 流失预测 → Slack 告警

## 导入方式

1. 打开 n8n 控制台 (http://localhost:5678)
2. 点击右上角 **Import from File**
3. 选择 `n8n-journey-analytics.json`
4. 激活工作流

## Webhook 端点

```
POST http://localhost:5678/webhook/customer-journey-events
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `OPENAI_API_KEY` | GPT-4 用于流失风险预测 |
| `SLACK_WEBHOOK_URL` | Slack 告警通知 |
| `POSTGRES_URL` | 事件数据持久化 |

## 事件格式

```json
{
  "userId": "user_123",
  "eventType": "page_view",
  "timestamp": "2026-07-29T10:00:00Z",
  "properties": {
    "page": "/products",
    "referrer": "google.com"
  },
  "source": "web"
}
```

## 支持的事件类型

- `page_view` — 页面访问
- `add_to_cart` — 加购
- `checkout` — 开始结算
- `purchase` — 完成购买
- `signup` — 注册
- `login` — 登录
- `custom` — 自定义事件

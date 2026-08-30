# 🛒 E-Commerce Automation — Integration

n8n 工作流集合，用于电商运营自动化。

## 📦 包含工作流

| 工作流 | 功能 | 触发方式 |
|--------|------|---------|
| `n8n-ecommerce-orders.json` | 订单自动处理 + 库存扣减 | Cron（每5分钟） |
| `n8n-inventory-monitor.json` | 库存智能监控 + 补货告警 | Cron（每1小时） |
| `n8n-price-optimizer.json` | 动态定价引擎 | Schedule + Webhook |
| `n8n-review-analyzer.json` | 评价情感分析 + 自动回复 | Webhook |

## 导入方法

1. 打开 n8n（`http://localhost:5678`）
2. 点击 **Import from File**
3. 选择对应 JSON 文件
4. 配置环境变量（见下文）
5. **Activate**

## 环境变量配置

在 n8n 凭证中设置以下变量：

```
ECOMMERCE_API_URL=https://api.your-platform.com
ECOMMERCE_API_KEY=your_api_key_here
ALERT_WEBHOOK_URL=https://hooks.slack.com/services/xxx
REORDER_THRESHOLD=10
INVENTORY_CHECK_INTERVAL=3600
```

## 订单处理流程

```
定时触发（每5分钟）
  → 获取新订单（去重）
  → 库存扣减（API 调用）
  → 告警通知（Slack/Discord）
  → 记录已处理订单 ID
```

## 适用平台

- **Shopify**：`https://{shop}.myshopify.com/admin/api/2024-01`
- **WooCommerce**：`https://your-store.com/wp-json/wc/v3`
- **淘宝开放平台**：需要申请 App Key + App Secret

---
*AI × 电商 = 7×24 无人值守运营*

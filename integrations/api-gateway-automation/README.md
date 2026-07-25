# API Gateway Automation — n8n Workflow

## 功能

- Kong/Traefik Admin API 读取当前限流状态
- 根据实时流量动态调整限流阈值
- 新 API Key 签发 → Vault 存储 → Slack 通知
- 高错误率触发 → 熔断 → 告警

## 使用方式

在 n8n 中导入 `api-gateway-workflow.json`，配置：
- Kong Admin URL / API Token（Credential）
- Redis 连接（限流计数）
- Slack Webhook URL（通知）

## 触发方式

- 手动触发（测试）
- 定时触发（每 5 分钟健康检查）
- Webhook 触发（Kong 日志事件）

# API Gateway Automation

> Kong / Traefik / Express Gateway — JWT 验证、限流、API 版本管理、熔断路由

## 核心能力

- **流量控制**：基于用户/路由/时间的限流策略，Redis 令牌桶算法
- **认证鉴权**：JWT / API Key / OAuth2 统一验证，支持多租户隔离
- **路由编排**：路径重写、灰度分流、A/B 测试、canary release
- **可观测性**：QPS/延迟/错误率埋点，自动告警阈值
- **安全防护**：WAF 规则、IP 黑名单、CORS 策略

## 工具清单

| 工具 | 说明 |
|---|---|
| Kong Gateway | API 网关核心 |
| Traefik | 云原生 Ingress |
| Redis | 限流计数 |
| Express/Gateway | 自建网关 |
| n8n | 策略配置下发 |

## n8n 集成

`integrations/api-gateway-automation/api-gateway-workflow.json`

- Webhook 触发 → 读取 Kong/Traefik Admin API
- 动态更新限流策略（Redis TTL）
- 新 API Key 签发 → 存储 Vault
- 异常流量 → 发送 Slack/PagerDuty 告警

## 快速开始

```bash
# Kong + Redis 限流示例
curl -X POST http://kong:8001/services/ \
  --data "name=my-service" \
  --data "url=http://backend:3000"

curl -X POST http://kong:8001/services/my-service/routes/ \
  --data "paths[]=/api/v1"

# 限流插件
curl -X POST http://kong:8001/services/my-service/plugins/ \
  --data "name=rate-limiting" \
  --data "config.minute=100" \
  --data "config.policy=redis"
```

## 使用场景

- 微服务统一入口
- 多租户 API 隔离与计费
- 灰度发布与流量镜像
- 外部合作 API 鉴权管理

## 相关技能

- `auth-automation` — JWT/OAuth2 实现
- `resilience-patterns` — 熔断降级
- `monitoring-alerting-automation` — 告警集成

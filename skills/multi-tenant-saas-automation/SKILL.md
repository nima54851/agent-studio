# Multi-Tenant SaaS Automation

> 多租户 SaaS 管理 — 租户隔离、订阅计费、用量追踪、White-label

## 核心能力

- **租户隔离**：数据库行级隔离 + Schema 隔离混合策略，Tenant ID 透传
- **订阅管理**：Stripe/Braintree 订阅创建/升级/降级/取消，自动到期提醒
- **用量计费**（Usage-Based Billing）：API 调用量/存储量 → Stripe Metered Billing
- **White-label**：自定义域名、CSS 主题、邮件模板，租户品牌独立
- **Tenant Onboarding**：注册 → 配置 → 引导 → 激活全流程自动化
- **租户健康分**：活跃度/付费率/支持工单 → AI 预警流失风险

## 工具清单

| 工具 | 说明 |
|---|---|
| Stripe | 订阅 + Metered Billing |
| PostgreSQL Row Security | 行级租户隔离 |
| Redis (Tenant Context) | 请求级别租户信息 |
| SendGrid / Postmark | 品牌化邮件 |
| n8n | 全生命周期自动化 |

## n8n 集成

`integrations/multi-tenant-saas-automation/multi-tenant-workflow.json`

- Stripe Webhook → 订阅状态同步 → 激活/暂停租户
- 用量上报 → Stripe Metered Billing → 生成发票
- 租户注册 → 自动创建 DB Schema → 初始化数据 → 发欢迎邮件
- 流失预警 → 自动发送挽留 Offer

## 数据库设计模式

```sql
-- Row-Level Security (PostgreSQL)
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON documents
  USING (tenant_id = current_setting('app.current_tenant')::uuid);

-- 用量记录
CREATE TABLE usage_records (
  id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL,
  metric_name TEXT NOT NULL,
  quantity INTEGER NOT NULL,
  recorded_at TIMESTAMPTZ DEFAULT now()
);
```

## 使用场景

- B2B SaaS 多租户计费
- 平台型产品（Marketplace）租户管理
- White-label 解决方案交付
- 用量驱动定价（Pay-as-you-go）

## 相关技能

- `auth-automation` — 租户认证
- `budget-management-automation` — 财务追踪
- `email-automation` — Onboarding 邮件序列

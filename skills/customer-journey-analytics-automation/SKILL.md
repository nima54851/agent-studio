# Customer Journey Analytics Automation

> 全链路用户行为分析：漏斗追踪、用户分群、流失预测、路径归因

## 功能概述

自动化采集、分析、可视化用户在产品中的完整行为路径，帮助产品团队识别转化瓶颈、优化用户体验、预测流失风险。

## 核心能力

### 📊 漏斗分析
- 定义任意转化漏斗（注册 → 浏览 → 加购 → 下单）
- 计算每步转化率、流失率、耗时中位数
- 自动识别高流失节点并标注

### 👥 用户分群
- 基于行为的 RFM 分群（Recency/Frequency/Monetary）
- 活跃度分群：新用户 / 活跃用户 / 沉默用户 / 流失用户
- 自定义分群规则（规则引擎 + AI 辅助）

### 🔮 流失预测
- 时序特征 + 行为特征建模
- 每日预测流失风险用户列表
- 自动触发挽留工作流（n8n → Email/推送/SMS）

### 🛤️ 路径归因
- Markov Chain 路径归因
- U 型归因（首末触点加权）
- 线性归因、时间衰减归因

### 📈 实时看板
- DAU/WAU/MAU 趋势
- 关键事件实时计数
- 异常波动告警（同比/环比）

## 技术架构

```
用户行为事件 (Web/Mobile SDK)
  → Kafka / SQS 事件流
  → Stream Processing (Flink/Spark Streaming)
  → ClickHouse / BigQuery 分析存储
  → AI 模型（流失预测、路径归因）
  → Grafana / Metabase 看板
  → n8n 自动化（告警、挽留触达）
```

## n8n 工作流

**Customer Journey Analytics Pipeline**
```json
// integrations/customer-journey-analytics-automation/n8n-journey-analytics.json
```

- 事件接收 → 数据清洗 → 漏斗计算 → 分群更新 → 流失预测 → 告警触达

## 集成

| 工具 | 用途 |
|------|------|
| PostHog | 行为事件采集 |
| Mixpanel | 移动端分析 |
| Amplitude | 产品分析 |
| Segment | CDP 数据汇聚 |
| BigQuery | 大规模数据仓库 |
| ClickHouse | 实时 OLAP |
| Grafana | 可视化看板 |
| n8n | 自动化触发 |

## 使用场景

1. **电商转化优化**：识别加购但未下单的用户，定向发券
2. **SaaS 留存分析**：预测 7 日流失用户，提前干预
3. **活动效果评估**：AB 测试期间追踪各路径转化贡献
4. **用户生命周期管理**：自动化用户分层运营策略

## 快速开始

```bash
# 1. 部署事件接收服务
docker run -d -p 8080:8080 journey-analytics/event-collector

# 2. 配置 n8n workflow
# 导入 integrations/customer-journey-analytics-automation/n8n-journey-analytics.json

# 3. 配置数据源
# POSTHOG_API_KEY=xxx
# GRAFANA_URL=https://grafana.example.com
```

## 输出示例

```
📊 漏斗报告 2026-07-29
Step 1: 访问商品页    10,000 (100%)
Step 2: 加入购物车     3,200 (32%)   ⚠️ -18% vs 上周
Step 3: 提交订单       1,800 (18%)
Step 4: 完成支付       1,440 (14.4%)

🔥 流失预警 (今日新识别)
- 高风险: 234 用户 (7日未活跃)
- 中风险: 1,892 用户 (3日未活跃)
- 已自动触发挽留流程: 234 用户
```

---

*版本 1.0 | 2026-07-29 | agent-studio*

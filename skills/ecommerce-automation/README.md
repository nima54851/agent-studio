# 🛒 E-Commerce Automation

AI 驱动的电商运营自动化技能包，覆盖订单、库存、价格、评价、物流全链路。

## 📦 包含内容

- **SKILL.md** — 技能定义与使用说明
- **n8n-ecommerce-orders.json** — 订单处理工作流（Shopify/WooCommerce 接入）
- **n8n-inventory-monitor.json** — 库存智能监控 + 补货告警工作流
- **n8n-price-optimizer.json** — 动态定价引擎工作流
- **n8n-review-analyzer.json** — 评价情感分析 + 自动回复工作流
- **scripts/ecommerce_monitor.py** — 电商监控主脚本
- **scripts/price_optimizer.py** — 动态定价引擎
- **scripts/review_analyzer.py** — NLP 评价分析
- **scripts/logistics_tracker.py** — 物流异常跟踪

## 🚀 快速开始

### n8n 工作流导入
1. 打开 n8n → Import from File
2. 选择 `n8n-ecommerce-orders.json`
3. 配置你的电商平台 API 凭证
4. Activate

### 命令行监控
```bash
pip install requests schedule python-dotenv
python3 scripts/ecommerce_monitor.py start
```

## 功能详情

### 订单自动化
- 订单创建 → 库存扣减 → 邮件通知 → 物流录入 全自动
- 异常订单自动标记 + 告警

### 库存监控
- 多 SKU 并发监控
- 低于阈值自动告警（Slack/Email/Telegram）
- 自动生成补货建议

### 动态定价
- 基于竞品价格、库存水平、季节性需求自动调整
- 支持价格下限保护

### 评价分析
- 中文/英文评价情感分类（正面/中性/负面）
- 负面评价自动回复模板 + 升级处理
- 评价摘要报告生成

## 配置说明

```bash
# .env
ECOMMERCE_API_KEY=your_api_key
ECOMMERCE_STORE_URL=https://your-store.com
ALERT_WEBHOOK=https://hooks.slack.com/services/xxx
REORDER_THRESHOLD=10
LOGISTICS_API_KEY=your_logistics_key
```

## 适用平台
- Shopify, WooCommerce, Magento
- 淘宝/天猫开放平台
- 京东商家开放平台
- 支持任意 REST API 的电商系统

---
*AI Agent × 电商 = 7×24 无人值守运营*

# 🛒 E-Commerce Automation Skill

自动处理电商运营全链路：订单处理、库存监控、价格动态调整、用户评价分析、物流跟踪告警。

## 能力矩阵

| 能力 | 描述 | n8n 节点 |
|------|------|---------|
| 订单自动处理 | 接收订单 → 库存扣减 → 发货通知 → 物流录入 | HTTP Request / Code |
| 库存智能监控 | 低于阈值自动告警 + 自动补货建议 | Schedule Trigger / Code |
| 价格动态调整 | 基于竞品价格、库存、需求弹性自动调价 | Code / HTTP Request |
| 评价 AI 分析 | NLP 情感分析 → 自动回复 → 问题升级 | AI Agent / Code |
| 物流异常告警 | 跟踪号异常 → 自动触发退款/重发流程 | Webhook / Code |

## 快速开始

### 1. 安装依赖
```bash
pip install requests schedule python-dotenv
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 填入：电商平台 API Key、告警渠道 webhook URL
```

### 3. 启动监控
```bash
python3 scripts/ecommerce_monitor.py start
```

## 目录结构
```
ecommerce-automation/
├── SKILL.md           # 本文件
├── README.md          # 详细文档
└── scripts/
    ├── ecommerce_monitor.py      # 订单/库存监控主脚本
    ├── price_optimizer.py        # 动态定价引擎
    ├── review_analyzer.py        # 评价情感分析
    └── logistics_tracker.py      # 物流跟踪
```

## 适用平台
- Shopify / WooCommerce / 淘宝开放平台 / 京东商家开放平台
- 通用 REST API 电商系统均可接入

## 示例场景

**场景：库存不足告警**
```python
# 当 SKU 库存低于阈值时，自动发送告警并建议补货
inventory_level = check_inventory(sku)
if inventory_level < REORDER_THRESHOLD:
    send_alert(f"⚠️ {sku} 库存不足: {inventory_level}，建议补货 {REORDER_QTY} 件")
    create_purchase_order(sku, REORDER_QTY)
```

---
*适用于电商运营自动化，AI Agent 驱动全链路降本增效*

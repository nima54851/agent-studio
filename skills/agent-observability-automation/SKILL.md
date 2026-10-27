# Agent Observability Automation

> 全面监控 AI Agent 的健康状态、性能指标、错误率与成本追踪

## 概述

Agent Observability Automation 提供端到端的 AI Agent 可观测性解决方案，涵盖日志采集、指标暴露、追踪关联和告警通知。

## 核心功能

- **指标采集**: 请求量、延迟分布、Token 消耗、成本估算、错误率
- **日志聚合**: 结构化日志 → OpenTelemetry → 统一存储
- **追踪关联**: Trace ID 贯穿 LLM 调用全链路
- **健康检查**: /health, /ready, /metrics 端点
- **告警规则**: 错误率阈值、延迟 P99、成本超限自动告警
- **Grafana 仪表盘**: 预置面板，快速上手

## 技术栈

- Prometheus + node-exporter（指标）
- Loki + Grafana（可观测性面板）
- OpenTelemetry SDK（追踪）
- n8n（告警路由 → Slack/Discord/Email）
- Python/JS（Instrumentation 库）

## 快速开始

```bash
# 1. 启动监控栈
docker-compose up -d prometheus loki grafana

# 2. 安装 Python instrumentation
pip install otel-sdk observability-kit

# 3. 接入现有 Agent
from observability import AgentObserver
observer = AgentObserver(endpoint="http://localhost:9090")
```

## 目录结构

```
skills/agent-observability-automation/
  SKILL.md              # 本文件
integrations/agent-observability-automation/
  docker-compose.yml    # 监控栈
  prometheus.yml        # 采集规则
  grafana-dashboard.json # 预置面板
  n8n-observability-workflow.json # 告警工作流
  py_instrument.py      # Python Agent 埋点
  js_instrument.js      # JS/TS Agent 埋点
```

## 告警规则示例

| 规则 | 阈值 | 动作 |
|------|------|------|
| 错误率 | > 5% / 5min | Slack @here |
| P99 延迟 | > 3000ms | PagerDuty |
| Token 超额 | > $10/天 | Email |
| Agent 无响应 | > 60s | Discord |

## 集成方式

```yaml
# prometheus.yml scrape target
- job_name: 'ai-agent'
  static_configs:
    - targets: ['agent:8000']
  metrics_path: '/metrics'
```

## 相关技能

- `logging-automation` — 日志采集
- `llm-ops-automation` — LLM 成本追踪
- `monitoring-alerting-automation` — 告警规则

---

*由 agent-studio 自动生成 | 2026-10-27*

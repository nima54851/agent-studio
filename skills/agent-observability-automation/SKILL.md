# Agent Observability Automation

## What It Does
Complete observability stack for AI agents: traces, metrics, logs, cost tracking, and performance dashboards — so you know exactly what your agents are doing and spending.

## Capabilities
- **Distributed tracing**: LangSmith / OpenTelemetry traces for every agent run
- **Cost tracking**: Per-agent, per-task, per-model cost with budget alerts
- **Latency monitoring**: P50/P95/P99 response times per skill/tool
- **Error rate tracking**: Failure classification (rate limit, auth, logic, timeout)
- **Token usage dashboard**: Daily/weekly/monthly token consumption by agent
- **Human-in-the-loop flags**: Detect when agent requests human approval
- **A/B performance comparison**: Compare agent versions by success rate + cost
- **Alerting**: PagerDuty/Slack alerts on anomalies (error spike, cost overrun, latency blowout)
- **SLO tracking**: Define SLOs (e.g., "95% of tasks complete in <30s") and track adherence

## Metrics Collected
| Metric | Description |
|--------|-------------|
| `agent.tasks.total` | Total tasks processed |
| `agent.tasks.success` | Successful completions |
| `agent.tasks.failed` | Failed tasks by error type |
| `agent.duration_ms` | Task duration histogram |
| `agent.tokens.used` | Total tokens per task |
| `agent.cost.usd` | Estimated cost in USD |
| `agent.hitl.count` | Human-in-the-loop triggers |

## Stack
- **Tracing**: LangSmith, OpenTelemetry, Jaeger
- **Metrics**: Prometheus + Grafana
- **Logs**: Loki / ELK
- **Alerts**: PagerDuty, Slack, Discord
- **Dashboards**: Grafana pre-built panels

## Setup
```bash
cp -r skills/agent-observability-automation $AGENT_SKILLS_DIR/
```

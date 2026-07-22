# Agent Observability — n8n Integration

## Workflow: Observability Data Pipeline

### Trigger
- Every agent task completion (webhook)
- Scheduled: daily metrics rollup

### Steps
1. **Agent task webhook** → capture trace, tokens, duration, error status
2. **Parse metadata** → extract agent ID, skill used, model, input/output size
3. **Calculate cost** → model pricing × token count
4. **Write to InfluxDB/Prometheus** → time-series metrics
5. **Log to Loki** → structured JSON logs
6. **Grafana dashboard** → auto-refresh dashboards
7. **Alert evaluation** → check SLO breach, cost threshold
8. **Route alert** → Slack (warning) / PagerDuty (critical)

### n8n Nodes
- Webhook (agent task events)
- Code (metrics parser)
- InfluxDB / Prometheus node
- Loki node (structured logging)
- Grafana node (dashboard refresh)
- Condition (SLO check)
- Slack / PagerDuty (alerts)

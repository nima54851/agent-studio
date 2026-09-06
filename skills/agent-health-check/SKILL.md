# Agent Health Check Skill

## Overview
Real-time health monitoring and self-healing for AI agents. Monitors uptime, response quality, tool availability, and automatic recovery when issues are detected.

## Features
- **Uptime Monitoring**: Track agent availability, response time, error rates
- **Tool Health**: Verify MCP tools, APIs, and external services are reachable
- **Response Quality**: Latency, token efficiency, error rate per session
- **Auto-healing**: Restart stuck agents, reset tool connections, clear memory leaks
- **Alerting**: Slack/Discord/PagerDuty alerts on health degradation
- **Dashboard**: Live health dashboard with Grafana-compatible metrics

## Health Checks
```bash
# Run health check
agent-health check --all

# Output
{
  "agent": "healthy",
  "uptime_ms": 86400000,
  "last_error": null,
  "tools": {
    "github": "ok",
    "memory": "ok",
    "web_search": "ok"
  },
  "avg_response_ms": 234,
  "error_rate": 0.001
}
```

## Auto-healing Actions
| Failure | Action |
|---------|--------|
| Tool timeout | Retry with backoff, mark degraded |
| Memory overflow | Flush old sessions, compact memory |
| Token limit | Trigger context summarization |
| Repeated errors | Restart agent, alert team |

## Prometheus Metrics
```
# HELP agent_health_status 1=healthy, 0=unhealthy
agent_health_status{service="github-automation"} 1

# HELP agent_response_time_ms Response latency
agent_response_time_ms{service="github-automation"} 234
```

## n8n Workflow
See `integrations/agent-health-check/health-monitor.json`

---

*Skill: agent-health-check | v1.0.0 | 2026-09-06*

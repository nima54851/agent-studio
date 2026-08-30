# Agent Swarm Orchestration — n8n Workflow

This workflow demonstrates a multi-agent swarm pattern using n8n:

1. **Supervisor Node** — receives task, spawns sub-tasks
2. **Fan-out** — distributes tasks to specialized agents (research, write, review)
3. **Wait for All** — collects all agent responses
4. **Aggregator** — synthesizes final output

## Nodes

| Node | Role |
|------|------|
| Webhook (trigger) | Receives task from OpenClaw / API |
| Supervisor | Parses task, assigns roles |
| Agent: Researcher | Searches web, reads docs |
| Agent: Writer | Drafts content based on research |
| Agent: Reviewer | Scores quality, flags issues |
| Aggregator | Combines all outputs into final response |
| Slack/Discord Node | Notifies on completion |

## Credentials

Requires:
- OpenAI API key (for LLM agents)
- Slack/Discord webhook URL (optional)

## Usage

Import into n8n, configure credentials, activate.

```bash
# Trigger the swarm
curl -X POST https://your-n8n-instance/webhook/agent-swarm \
  -H "Content-Type: application/json" \
  -d '{"task": "Write a report on AI agents", "depth": "detailed"}'
```

## Response

```json
{
  "supervisor": "Task assigned to 3 agents",
  "research": { "status": "complete", "sources": 5 },
  "write": { "status": "complete", "word_count": 850 },
  "review": { "score": 8.2, "flags": [] },
  "aggregated": { "ready": true, "output": "..." }
}
```

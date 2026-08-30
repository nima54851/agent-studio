# Agent Swarm Orchestration

Multi-agent coordination system for autonomous task distribution, consensus building, and collective problem-solving.

## Overview

This skill enables a supervisor agent to spawn, coordinate, and manage a swarm of specialized sub-agents. Agents communicate via a shared message bus, vote on decisions, and can delegate tasks dynamically.

## Core Patterns

### Supervisor Pattern
One agent coordinates, assigns tasks to specialized agents, and aggregates results.

### Debate Pattern
Multiple agents argue different positions; a moderator agent synthesizes the final answer.

### Voting Pattern
Agents vote on a decision; majority wins (configurable threshold).

### Fan-out / Fan-in
One task is distributed across N agents, results are aggregated.

## Architecture

```
┌──────────────┐
│  Supervisor  │  ← coordinates the swarm
└──────┬───────┘
       │ assigns / aggregates
  ┌────▼────┐  ┌─────────────┐
  │ Agent A │  │  Agent B    │
  │(research)│  │ (execution) │
  └────┬────┘  └──────┬──────┘
       │               │
       └───────┬───────┘
               │ results
         ┌─────▼─────┐
         │ Aggregator │
         │ (synthesis)│
         └───────────┘
```

## Configuration

```json
{
  "max_agents": 5,
  "consensus_threshold": 0.6,
  "timeout_seconds": 120,
  "retry_on_failure": true,
  "max_retries": 2
}
```

## Usage in OpenClaw

```javascript
// Spawn a swarm of agents
const swarm = await sessions_spawn({
  agents: [
    { id: 'researcher', task: 'Research topic X' },
    { id: 'writer', task: 'Write article about findings' },
    { id: 'reviewer', task: 'Review and rate the article' }
  ],
  coordination: 'supervisor',
  aggregate: true
});
```

## Integration

Integrates with n8n for workflow orchestration of multi-agent pipelines. See `integrations/agent-swarm-orchestration/n8n-swarm-workflow.json`.

## Files

- `skills/agent-swarm-orchestration/SKILL.md` — this file
- `integrations/agent-swarm-orchestration/n8n-swarm-workflow.json` — n8n workflow
- `scripts/swarm_simulator.py` — standalone Python demo

## License

MIT

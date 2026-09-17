# Agent Fallback Automation Skill

**Version:** 1.0.0  
**Author:** agent-studio  
**Tags:** agent-automation, resilience, error-handling, reliability  

## Overview

Intelligent fallback system for AI agents that gracefully degrades when primary services fail, routes to backup models, queues requests during outages, and maintains service continuity.

## Features

- **Multi-Model Fallback:** Primary → Secondary → Tertiary model routing
- **Circuit Breaker Pattern:** Auto-disable failing services after threshold
- **Request Queuing:** Queue requests during outages, process when restored
- **Graceful Degradation:** Return partial results or cached responses
- **Health Monitoring:** Real-time service health dashboard
- **Auto-Recovery:** Automatically re-enable services after recovery

## Fallback Chain

```
User Request → Primary Model (OpenAI)
    ↓ [failure/timeout]
Secondary Model (Anthropic)
    ↓ [failure/timeout]
Tertiary Model (Local/Ollama)
    ↓ [all failed]
Cached Response / Queue / Apology
```

## Usage

```python
from agent_fallback import FallbackAgent

agent = FallbackAgent(
    primary="gpt-4",
    secondary="claude-3-haiku",
    tertiary="ollama/llama3"
)

response = agent.chat("Your prompt here")
print(response.content)
```

## Configuration

```json
{
  "circuit_breaker": {
    "failure_threshold": 5,
    "timeout_seconds": 60,
    "half_open_max_calls": 3
  },
  "queue": {
    "max_size": 1000,
    "retry_interval_seconds": 30
  }
}
```

## n8n Workflow

See `integrations/agent-fallback-automation/n8n-fallback-workflow.json`

# Agent Memory Optimizer

> Optimize AI agent memory usage: context window management, summarization strategies, and memory eviction policies.

## What It Does

Automatically manages agent conversation context to stay within token limits while preserving the most relevant information.

## Core Capabilities

- **Context Window Tracking**: Monitor token usage in real-time; trigger cleanup before overflow
- **Smart Summarization**: Compress older messages using LLM summarization while preserving key facts
- **Memory Tiering**: Hot (recent), Warm (important), Cold (archived) — auto-promote/demote
- **Eviction Policies**: LRU, importance-score-based, or hybrid
- **Memory Compression**: Delta encoding for repeated structures, deduplication

## Usage



## Example Workflow

1. Agent sends messages to optimizer endpoint
2. Optimizer tracks tokens, applies summarization when threshold reached
3. Compressed context returned to agent
4. Original messages archived to cold storage

## Eviction Strategy

| Policy | Best For | Tradeoff |
|--------|----------|----------|
| LRU | Short conversations | May lose important facts |
| Importance Score | Complex tasks | Requires scoring model |
| Hybrid | Production use | More compute overhead |

## Prompt Template

```
You have {remaining_tokens} tokens remaining.
Memory summary: {compressed_context}
Recent messages: {recent_messages}
Task: {current_task}
```

## Related Skills

- agent-memory-system
- agent-memory
- llm-ops-automation

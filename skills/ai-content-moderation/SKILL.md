# AI Content Moderation

> Automated content moderation pipeline — toxicity detection, NSFW filtering, hate speech classification, and policy enforcement via n8n + OpenClaw Agent.

## What it does

- **Multi-model analysis**: Run content through toxicity, hate speech, sexual content, and violence classifiers
- **AI judgment**: Use LLM to apply nuanced policy (not just binary — context-aware decisions)
- **User appeal flow**: Flagged content → user notification → appeal form → AI re-review
- **Dashboard**: Moderation stats — top violations, trending terms, moderation latency
- **Auto-actions**: Shadow-ban (soft delete), hard delete, flag for human review, or approve
- **Audit log**: Full moderation trail for compliance (SOC2/GDPR)

## Moderation Policy Matrix

| Content Type | Confidence ≥ 0.85 | Confidence 0.6–0.85 | Confidence < 0.6 |
|---|---|---|---|
| NSFW | Hard delete | Flag for review | AI re-judge |
| Hate speech | Hard delete | Flag for review | AI re-judge |
| Toxicity | Soft delete | Warn user | Approve |
| Violence threat | Hard delete + alert | Flag + alert | AI re-judge |
| Spam | Hard delete | — | — |

## n8n Workflow

```json
// integrations/ai-content-moderation/moderation-pipeline.json
{
  "name": "Content Moderation Pipeline",
  "nodes": [
    {"type": "Webhook", "parameters": {"httpMethod": "POST", "path": "moderation"}},
    {"type": "HTTP Request", "parameters": {"url": "https://api.openai.com/v1/moderations", "authentication": "genericCredentialType", "genericAuthType": "bearerAuth"}},
    {"type": "Code", "parameters": {"js": "const r = $json.results[0]; const flags = Object.entries(r.categories).filter(([k,v])=>v).map(([k])=>k); return [{flags, score: r.category_scores, passed: flags.length===0}];", "name": "Parse Flags"}},
    {"type": "IF", "parameters": {"conditions": [{"id": "passed", "value": false}]}},
    {"type": "LLM Chain", "parameters": {"model": "gpt-4o", "prompt": "Context: {{ $json.flags }}. Should this content be deleted, warned, or approved? Be concise, apply strict policy."}},
    {"type": "Slack Message", "parameters": {"channel": "#moderation-alerts", "text": "⚠️ Flagged: {{ $json.flags.join(', ') }} — Action: {{ $json.action }}"}}
  ]
}
```

## Python SDK Example

```python
# scripts/moderation_client.py
from openai import OpenAI

client = OpenAI()

def moderate_content(text: str) -> dict:
    result = client.moderations.create(input=text)
    r = result.results[0]
    flags = {k: v for k, v in r.categories.items() if v}
    return {
        "passed": len(flags) == 0,
        "flags": list(flags.keys()),
        "scores": {k: getattr(r.category_scores, k) for k in flags}
    }

def moderate_batch(texts: list[str], threshold: float = 0.85) -> list[dict]:
    results = client.moderations.create(input=texts)
    outputs = []
    for r in results.results:
        flags = {k: getattr(r.categories, k) for k in dir(r.categories) if not k.startswith('_')}
        active = {k: v for k, v in flags.items() if v and getattr(r.category_scores, k, 0) >= threshold}
        outputs.append({"passed": not active, "flags": list(active.keys())})
    return outputs
```

## Dashboard Metrics

| Metric | Target |
|---|---|
| Moderation latency | < 500ms |
| Auto-action accuracy | > 95% |
| False positive rate | < 3% |
| Human review queue size | < 50 items/day |

## Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | For moderation API |
| `SLACK_WEBHOOK` | Alert webhook |
| `DB_CONNECTION` | Moderation audit DB |
| `HUMAN_REVIEW_WEBHOOK` | Manual review queue URL |

## Related Skills

- [Sentiment Analysis Automation](../sentiment-analysis-automation/SKILL.md) — emotion detection
- [Customer Support Automation](../customer-support-automation/SKILL.md) — user communication
- [Compliance Automation](../compliance-automation/SKILL.md) — audit trail & GDPR

---

*Part of [agent-studio](https://github.com/nima54851/agent-studio) · Auto-generated 2026-07-24*

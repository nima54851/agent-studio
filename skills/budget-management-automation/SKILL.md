# Budget Management Automation

> AI-powered financial planning, expense tracking, forecasting, and anomaly alerting via n8n + OpenClaw Agent.

## What it does

- **Expense ingestion**: Read from bank CSVs, Stripe, PayPal, Notion tables, or Google Sheets
- **AI categorization**: Auto-classify transactions (travel, SaaS, infrastructure, marketing)
- **Forecasting**: LLM reads 3-month history → projects next 30/60/90 days spend
- **Anomaly detection**: Flag unusual spikes (>2σ from category average)
- **Budget alerts**: Slack/Email/Push when category hits 80%/100% threshold
- **Multi-currency**: Auto-convert to base currency (USD) using live FX rates

## n8n Workflow

```json
// integrations/budget-management-automation/budget-forecast.json
{
  "name": "Budget Forecast Pipeline",
  "nodes": [
    {"type": "Schedule Trigger", "parameters": {"rule": {"interval": [{"field": "day", "hours": 9}]}}},
    {"type": "Google Sheets", "parameters": {"operation": "readRows", "sheet": "Expenses"}},
    {"type": "Code", "parameters": {"js": "const rows = $json; const total = rows.reduce((s,r)=>s+(r.amount||0),0); return [{total, count: rows.length}];", "name": "Aggregate Spend"}},
    {"type": "LLM Chain", "parameters": {"model": "gpt-4o", "prompt": "Based on these monthly expenses (in USD): {{ $json.total }}. Provide a 30/60/90 day forecast and 3 cost-saving recommendations."}},
    {"type": "Slack Message", "parameters": {"channel": "#finops", "text": "📊 Forecast: {{ $json.forecast }}"}}
  ]
}
```

## CSV Import Example

```python
# scripts/budget_csv_importer.py
import csv, json, requests

def import_transactions(csv_path: str, categories: list[str]) -> dict:
    """Import transactions and let AI categorize them."""
    transactions = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append({
                "date": row["Date"],
                "amount": float(row["Amount"]),
                "merchant": row["Description"],
            })

    payload = {
        "model": "gpt-4o",
        "messages": [{
            "role": "user",
            "content": f"""Categorize these transactions into one of: {categories}.
            Return JSON array with fields: date, amount, merchant, category.
            Transactions: {json.dumps(transactions[:50])}"""
        }]
    }
    # ... send to OpenAI / OpenClaw
    return categorized
```

## Budget Alert Thresholds

| Category | Monthly Budget | 80% Alert | 100% Alert |
|---|---|---|---|
| Infrastructure | $2,000 | Slack #finops | PagerDuty |
| Marketing | $1,500 | Email | Slack |
| SaaS Subscriptions | $500 | Slack #finops | — |

## Environment Variables

| Variable | Description |
|---|---|
| `STRIPE_API_KEY` | Stripe secret key |
| `NOTION_TOKEN` | Notion integration token |
| `GOOGLE_SHEETS_ID` | Spreadsheet ID |
| `SLACK_WEBHOOK` | Slack webhook for alerts |
| `BASE_CURRENCY` | Default: USD |

## Related Skills

- [Data Processing Automation](../data-processing-automation/SKILL.md) — CSV/ETL
- [Cross-Platform Notification](../cross-platform-notification/SKILL.md) — multi-channel alerts
- [Cost Optimization Automation](../cost-optimization-automation/SKILL.md) — cloud spend

---

*Part of [agent-studio](https://github.com/nima54851/agent-studio) · Auto-generated 2026-07-24*

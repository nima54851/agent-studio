# AI SQL Query Automation

> Describe your data need in plain English — AI generates optimized SQL, executes it, and returns results.

## What It Does

Natural language → SQL query → execution → formatted results. Supports PostgreSQL, MySQL, SQLite, BigQuery.

## Core Capabilities

- **NL to SQL**: GPT-4/Claude generates SQL from English descriptions
- **Query Validation**: Syntax check + explain plan before execution
- **Auto-index Hints**: Suggests indexes based on query patterns
- **Result Formatting**: JSON, CSV, markdown table, or chart
- **Query History**: Track all queries with timestamps and results

## Usage

```bash
# Interactive mode
python3 sql_query.py ask --question "Show daily revenue for last 7 days"

# Direct SQL
python3 sql_query.py exec --sql "SELECT * FROM orders LIMIT 10"

# Schema introspection
python3 sql_query.py schema --tables orders,customers
```

## n8n Workflow

See `../integrations/ai-sql-query-automation/` for the full workflow:
- User input → LLM → SQL generation → validation → execution → result formatting → notification

## Security

- **Never** expose DB credentials in plain text — use n8n credentials
- All queries are logged with user, timestamp, SQL, and execution time
- Rate limiting: max 10 queries/minute per user

> Part of [agent-studio](https://github.com/nima54851/agent-studio) — AI Agent Skills Marketplace

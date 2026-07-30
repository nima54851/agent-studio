# Database Sharding Automation

> AI-powered horizontal sharding strategy — from single-node to distributed. Key selection, shard mapping, rebalancing, and migration with zero-downtime.

## What It Does

- **Shard Strategy**: Range-based, hash-based, directory-based sharding
- **Key Selection**: Analyze query patterns, cardinality, hot-spot detection with AI
- **Migration Planner**: Zero-downtime migration plan with rollback capability
- **Rebalancer**: Automatic shard rebalancing when data skew exceeds threshold
- **Consistency Checker**: Verify cross-shard integrity post-migration

## Skill Capabilities

- Analyze existing schema and query patterns to recommend shard key
- Generate migration SQL with dual-write phase
- Monitor shard sizes and rebalance on demand
- Support PostgreSQL Citus, MySQL sharding, MongoDB sharded clusters
- SLO gates: validate latency, error rate, data integrity after each phase

## Files

- `SKILL.md` — This file
- `shard_planner.py` — Shard strategy selector (range/hash/directory)
- `migration_runner.py` — Zero-downtime migration executor
- `shard_monitor.py` — Shard health, size tracking, rebalancing trigger

## Setup

```bash
pip install sqlalchemy psycopg2-binary pymongo tabulate
```

## Usage

```python
from shard_planner import ShardPlanner

planner = ShardPlanner(db_type="postgresql", connection_string="postgresql://...")
strategy = planner.analyze_and_recommend(
    table_name="orders",
    query_patterns=["SELECT * FROM orders WHERE user_id=?", "SELECT * FROM orders WHERE created_at>?"]
)
print(strategy.recommended_key, strategy.shard_count, strategy.reasoning)
```

## Migration Flow

```
Phase 1: Dual-write ON  (write to old + new shards)
Phase 2: Backfill       (copy existing data in batches)
Phase 3: Verify         (checksum cross-shard integrity)
Phase 4: Cutover        (switch reads to new shards)
Phase 5: Cleanup        (drop old tables, disable dual-write)
```

## n8n Integration

Import `n8n-db-sharding-migration.json` to automate migration:
- Cron trigger → read migration state → execute phase → verify integrity → Slack alert

## OpenClaw Integration

```python
# skill.py
async def plan_sharding(context):
    strategy = planner.analyze_and_recommend(
        table_name=context.table_name,
        query_patterns=context.query_patterns
    )
    return {"strategy": strategy.to_dict()}
```

---

*Part of [agent-studio](https://github.com/nima54851/agent-studio) · Built by 灵犀 AI*

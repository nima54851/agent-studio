"""
Database Sharding Planner
Analyzes query patterns and table statistics to recommend optimal shard strategy.
"""

import re
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from collections import Counter


class ShardStrategy(Enum):
    HASH = "hash"
    RANGE = "range"
    DIRECTORY = "directory"
    GEO = "geo"


@dataclass
class ShardPlan:
    strategy: ShardStrategy
    shard_key: str
    shard_count: int
    reasoning: str
    estimated_skew: float  # 0=perfect, 1=highly skewed
    hot_spots: list[str] = field(default_factory=list)
    migration_complexity: str = "medium"  # low/medium/high


class ShardPlanner:
    """
    Analyzes table schemas and query patterns to recommend a sharding strategy.
    """

    def __init__(self, db_type: str = "postgresql"):
        self.db_type = db_type

    def analyze_and_recommend(
        self, table_name: str, query_patterns: list[str], cardinality: Optional[int] = None
    ) -> ShardPlan:
        """
        Main entry point. Pass in table name and sample query patterns.
        Returns a ShardPlan with recommended strategy and shard key.
        """
        # Extract column references from queries
        referenced_cols = self._extract_columns(query_patterns)

        # Determine best shard key
        shard_key = self._select_shard_key(table_name, referenced_cols, cardinality)

        # Choose strategy
        strategy = self._choose_strategy(shard_key, query_patterns, referenced_cols)

        # Estimate skew
        skew = self._estimate_skew(shard_key, cardinality)

        # Find hot spots
        hot_spots = self._detect_hotspots(query_patterns, referenced_cols)

        # Migration complexity
        complexity = self._assess_migration_complexity(strategy, query_patterns)

        reasoning = self._build_reasoning(strategy, shard_key, skew, hot_spots)

        return ShardPlan(
            strategy=strategy,
            shard_key=shard_key,
            shard_count=self._recommended_shard_count(shard_key, cardinality),
            reasoning=reasoning,
            estimated_skew=round(skew, 3),
            hot_spots=hot_spots,
            migration_complexity=complexity,
        )

    def _extract_columns(self, query_patterns: list[str]) -> Counter:
        """Extract column names referenced in WHERE/JOIN/ON clauses."""
        cols = Counter()
        for q in query_patterns:
            # Match common SQL patterns: WHERE user_id=, JOIN ... ON a=b, ORDER BY ...
            where_cols = re.findall(r"(?:WHERE|AND|OR)\s+(\w+)\s*[=<>]", q, re.IGNORECASE)
            join_cols = re.findall(r"(?:JOIN|ON)\s+.*?(\w+)\s*=", q, re.IGNORECASE)
            order_cols = re.findall(r"ORDER\s+BY\s+(\w+)", q, re.IGNORECASE)
            cols.update(where_cols)
            cols.update(join_cols)
            cols.update(order_cols)
        return cols

    def _select_shard_key(
        self, table_name: str, referenced_cols: Counter, cardinality: Optional[int] = None
    ) -> str:
        """Select the best shard key based on query frequency and cardinality."""
        # Prefer high-frequency, high-cardinality columns
        if not referenced_cols:
            # Fallback heuristics
            if "user_id" in table_name.lower():
                return "user_id"
            return "id"

        # Top referenced column with high cardinality is the best shard key
        candidates = []
        for col, freq in referenced_cols.most_common(10):
            card = cardinality or 10000
            score = freq * math.log(card + 1)
            candidates.append((col, score))

        candidates.sort(key=lambda x: -x[1])
        return candidates[0][0] if candidates else "id"

    def _choose_strategy(
        self, shard_key: str, query_patterns: list[str], referenced_cols: Counter
    ) -> ShardStrategy:
        """
        Choose sharding strategy based on key characteristics and query patterns.
        """
        # Range-based is good for time-series (created_at, date, timestamp)
        time_keywords = {"created_at", "updated_at", "date", "timestamp", "time", "month", "year"}
        if shard_key.lower() in time_keywords or any(k in " ".join(query_patterns).lower() for k in time_keywords):
            return ShardStrategy.RANGE

        # Geo keys work well with directory-based
        geo_keywords = {"region", "country", "city", "latitude", "longitude", "location"}
        if shard_key.lower() in geo_keywords:
            return ShardStrategy.GEO

        # High-cardinality user/entity IDs → hash sharding
        return ShardStrategy.HASH

    def _estimate_skew(self, shard_key: str, cardinality: Optional[int] = None) -> float:
        """
        Estimate data skew. 0 = perfectly uniform, 1 = highly skewed.
        Uses heuristics based on key type.
        """
        hot_keys = {"region", "country", "category", "status", "type"}
        if shard_key.lower() in hot_keys:
            return 0.65  # Categorical keys often have skewed distribution
        if cardinality and cardinality < 100:
            return 0.5   # Low cardinality → unavoidable skew
        return 0.15      # Hash or high-cardinality → low skew

    def _detect_hotspots(self, query_patterns: list[str], referenced_cols: Counter) -> list[str]:
        """Detect hot spots — frequently accessed single values."""
        hot_spots = []
        for q in query_patterns:
            # Match WHERE key = 'constant_value' (potential hot spot)
            matches = re.findall(r"(?:WHERE|AND)\s+\w+\s*=\s*'([^']+)'", q, re.IGNORECASE)
            hot_spots.extend(matches[:3])  # Limit to top 3 per pattern
        return list(set(hot_spots[:10]))  # Deduplicate, max 10

    def _assess_migration_complexity(self, strategy: ShardStrategy, query_patterns: list[str]) -> str:
        """Assess how complex the migration will be."""
        has_joins = any("JOIN" in q.upper() for q in query_patterns)
        has_aggs = any("GROUP BY" in q.upper() for q in query_patterns)

        if has_joins or has_aggs:
            return "high"
        if strategy in (ShardStrategy.DIRECTORY, ShardStrategy.GEO):
            return "medium"
        return "low"

    def _recommended_shard_count(self, shard_key: str, cardinality: Optional[int] = None) -> int:
        """Recommend number of shards based on data size."""
        # Rule of thumb: 50GB per shard, start with 4 shards minimum
        # Adjust based on cardinality
        if cardinality and cardinality > 10_000_000:
            return 16
        elif cardinality and cardinality > 1_000_000:
            return 8
        return 4

    def _build_reasoning(
        self, strategy: ShardStrategy, shard_key: str, skew: float, hot_spots: list[str]
    ) -> str:
        parts = [f"Strategy: {strategy.value.upper()} sharding on key `{shard_key}`."]
        if skew < 0.2:
            parts.append("Estimated data distribution is balanced (low skew).")
        elif skew < 0.5:
            parts.append("Moderate skew expected — monitor shard sizes.")
        else:
            parts.append("⚠️ High skew risk — consider composite shard key or rebalancing.")
        if hot_spots:
            parts.append(f"Hot spots detected: {', '.join(hot_spots[:3])}")
        return " ".join(parts)

    def generate_create_shards_sql(self, plan: ShardPlan, base_table: str) -> list[str]:
        """Generate SQL to create sharded tables."""
        sqls = []
        for i in range(plan.shard_count):
            if plan.strategy == ShardStrategy.HASH:
                shard_name = f"{base_table}_shard_{(i + 1):02d}"
            elif plan.strategy == ShardStrategy.RANGE:
                shard_name = f"{base_table}_shard_{(i + 1):02d}"
            else:
                shard_name = f"{base_table}_shard_{(i + 1):02d}"

            sql = f"""-- Shard {i + 1}/{plan.shard_count}
CREATE TABLE IF NOT EXISTS {shard_name} (LIKE {base_table} INCLUDING ALL);
-- Add shard-specific constraint for range sharding
ALTER TABLE {shard_name} ADD CONSTRAINT {shard_name}_check
CHECK ({plan.shard_key} BETWEEN {i * (10**6)} AND {(i + 1) * (10**6)});
"""
            sqls.append(sql)
        return sqls


if __name__ == "__main__":
    planner = ShardPlanner("postgresql")

    queries = [
        "SELECT * FROM orders WHERE user_id = ?",
        "SELECT * FROM orders WHERE user_id = ? AND status = 'pending'",
        "SELECT * FROM orders WHERE created_at > '2026-01-01' ORDER BY created_at DESC",
        "SELECT COUNT(*) FROM orders WHERE region = 'APAC'",
    ]

    plan = planner.analyze_and_recommend(
        table_name="orders",
        query_patterns=queries,
        cardinality=5_000_000,
    )

    print("=== Shard Plan ===")
    print(f"Strategy:   {plan.strategy.value}")
    print(f"Shard Key:  {plan.shard_key}")
    print(f"Shard Count:{plan.shard_count}")
    print(f"Skew:       {plan.estimated_skew}")
    print(f"Complexity: {plan.migration_complexity}")
    print(f"Reasoning:  {plan.reasoning}")
    if plan.hot_spots:
        print(f"Hot Spots:  {', '.join(plan.hot_spots)}")

    print("\n=== Shard DDL ===")
    for sql in planner.generate_create_shards_sql(plan, "orders")[:2]:
        print(sql)

"""
A/B Test Runner for Recommendation Strategies
Tracks click-through rate (CTR), conversion rate, and statistical significance.
"""

import json
import math
import time
from dataclasses import dataclass, field
from typing import Optional
from collections import defaultdict


@dataclass
class Variant:
    name: str
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    revenue: float = 0.0
    rewards: list = field(default_factory=list)

    @property
    def ctr(self) -> float:
        return self.clicks / self.impressions if self.impressions > 0 else 0.0

    @property
    def conversion_rate(self) -> float:
        return self.conversions / self.clicks if self.clicks > 0 else 0.0

    @property
    def avg_reward(self) -> float:
        return sum(self.rewards) / len(self.rewards) if self.rewards else 0.0


class ABTestRunner:
    """
    Multi-arm bandit A/B test runner for recommendation strategies.
    Supports UCB1, Thompson Sampling, and simple epsilon-greedy.
    """

    def __init__(self, test_id: str, variants: list[str], strategy: str = "thompson"):
        self.test_id = test_id
        self.variants = {v: Variant(name=v) for v in variants}
        self.strategy = strategy
        self.total_impressions = 0
        self.start_time = time.time()
        self._epsilon = 0.1

    def select_variant(self) -> str:
        """Select which variant to show based on the active strategy."""
        if self.strategy == "thompson":
            return self._thompson_sample()
        elif self.strategy == "ucb1":
            return self._ucb1()
        elif self.strategy == "epsilon_greedy":
            return self._epsilon_greedy()
        else:
            return list(self.variants.keys())[0]

    def _thompson_sample(self) -> str:
        """Thompson Sampling: sample from posterior beta distribution."""
        import random
        best_variant = None
        best_score = -1
        for name, variant in self.variants.items():
            alpha = variant.clicks + 1
            beta = (variant.impressions - variant.clicks) + 1
            score = random.betavariate(alpha, beta)
            if score > best_score:
                best_score = score
                best_variant = name
        return best_variant

    def _ucb1(self) -> str:
        """Upper Confidence Bound 1."""
        best_variant = None
        best_ucb = -1
        for name, variant in self.variants.items():
            if variant.impressions == 0:
                return name
            exploitation = variant.clicks / variant.impressions
            exploration = math.sqrt(2 * math.log(self.total_impressions + 1) / variant.impressions)
            ucb = exploitation + exploration
            if ucb > best_ucb:
                best_ucb = ucb
                best_variant = name
        return best_variant

    def _epsilon_greedy(self) -> str:
        """Epsilon-greedy: explore with probability epsilon, exploit otherwise."""
        import random
        if random.random() < self._epsilon:
            return random.choice(list(self.variants.keys()))
        best = max(self.variants.values(), key=lambda v: v.ctr)
        return best.name

    def record_impression(self, variant: str, product_ids: list[str]):
        """Record an impression for a variant."""
        self.variants[variant].impressions += 1
        self.total_impressions += 1

    def record_click(self, variant: str):
        """Record a click for a variant."""
        self.variants[variant].clicks += 1

    def record_conversion(self, variant: str, revenue: float = 0.0):
        """Record a conversion/reward for a variant."""
        self.variants[variant].conversions += 1
        self.variants[variant].revenue += revenue
        self.variants[variant].rewards.append(revenue or 1.0)

    def statistical_significance(self, control: str, treatment: str, metric: str = "ctr") -> dict:
        """Calculate Z-test statistical significance between two variants."""
        a = self.variants[control]
        b = self.variants[treatment]

        if metric == "ctr":
            p1 = a.ctr
            p2 = b.ctr
            n1 = a.impressions
            n2 = b.impressions
        else:
            p1 = a.conversion_rate
            p2 = b.conversion_rate
            n1 = a.clicks
            n2 = b.clicks

        if n1 == 0 or n2 == 0:
            return {"significant": False, "p_value": None, "message": "Not enough data"}

        pooled = (a.clicks + b.clicks) / (a.impressions + b.impressions + 1e-9)
        se = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
        z = (p2 - p1) / (se + 1e-9)
        p_value = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))

        return {
            "control_variant": control,
            "treatment_variant": treatment,
            "metric": metric,
            "control_value": round(p1, 5),
            "treatment_value": round(p2, 5),
            "lift_percent": round((p2 - p1) / (p1 + 1e-9) * 100, 2),
            "z_score": round(z, 3),
            "p_value": round(p_value, 5),
            "significant": p_value < 0.05,
            "confidence": "95%" if p_value < 0.05 else "Not significant",
        }

    def get_report(self) -> dict:
        """Generate a full A/B test report."""
        elapsed_hours = (time.time() - self.start_time) / 3600
        return {
            "test_id": self.test_id,
            "strategy": self.strategy,
            "elapsed_hours": round(elapsed_hours, 1),
            "total_impressions": self.total_impressions,
            "variants": {
                name: {
                    "impressions": v.impressions,
                    "clicks": v.clicks,
                    "ctr": round(v.ctr * 100, 2),
                    "conversions": v.conversions,
                    "conversion_rate": round(v.conversion_rate * 100, 2),
                    "revenue": round(v.revenue, 2),
                    "avg_reward": round(v.avg_reward, 3),
                    "share_percent": round(v.impressions / self.total_impressions * 100, 1) if self.total_impressions else 0,
                }
                for name, v in self.variants.items()
            },
        }

    def save(self, path: str = "/tmp/ab_test_state.json"):
        """Persist test state."""
        data = {
            "test_id": self.test_id,
            "strategy": self.strategy,
            "total_impressions": self.total_impressions,
            "start_time": self.start_time,
            "variants": {
                name: {
                    "impressions": v.impressions,
                    "clicks": v.clicks,
                    "conversions": v.conversions,
                    "revenue": v.revenue,
                    "rewards": v.rewards[-100:],
                }
                for name, v in self.variants.items()
            },
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, path: str, variants: list[str]) -> "ABTestRunner":
        """Load a saved test state."""
        with open(path) as f:
            data = json.load(f)
        runner = cls(data["test_id"], variants, data["strategy"])
        runner.total_impressions = data["total_impressions"]
        runner.start_time = data["start_time"]
        for name, vdata in data["variants"].items():
            if name in runner.variants:
                runner.variants[name].impressions = vdata["impressions"]
                runner.variants[name].clicks = vdata["clicks"]
                runner.variants[name].conversions = vdata["conversions"]
                runner.variants[name].revenue = vdata["revenue"]
                runner.variants[name].rewards = vdata["rewards"]
        return runner


if __name__ == "__main__":
    # Demo
    test = ABTestRunner("rec-strategy-v1", ["collaborative", "content_hybrid", "random_baseline"], strategy="thompson")
    import random
    for _ in range(500):
        variant = test.select_variant()
        test.record_impression(variant, ["p1", "p2"])
        if random.random() < 0.2:
            test.record_click(variant)
        if random.random() < 0.1:
            test.record_conversion(variant, revenue=round(random.uniform(10, 100), 2))

    report = test.get_report()
    print(json.dumps(report, indent=2))
    sig = test.statistical_significance("collaborative", "content_hybrid")
    print("\nStatistical Significance:")
    print(json.dumps(sig, indent=2))

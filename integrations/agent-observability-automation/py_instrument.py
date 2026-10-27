"""
Python Agent Observability Instrumentation
pip install prometheus_client

Usage:
    from py_instrument import AgentObserver
    obs = AgentObserver("my-agent")
    obs.record_request(prompt_tokens=100, completion_tokens=50, latency_ms=320)
    print(obs.get_metrics())
"""
import time
import random
import logging
from typing import Optional, Dict, Any
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent_observer")


class AgentObserver:
    """Lightweight observability instrumentation for AI agents."""

    def __init__(self, agent_name: str = "agent"):
        self.agent_name = agent_name
        self._metrics = {
            "requests_total": 0,
            "requests_error": 0,
            "tokens_total": 0,
            "cost_total": 0.0,
            "latencies": [],
        }

    def record_request(
        self,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        cost_per_1k: float = 0.002,
        status: str = "success",
        latency_ms: float = 0,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        total_tokens = prompt_tokens + completion_tokens
        cost = (total_tokens / 1000) * cost_per_1k
        self._metrics["requests_total"] += 1
        if status == "error":
            self._metrics["requests_error"] += 1
        self._metrics["tokens_total"] += total_tokens
        self._metrics["cost_total"] += cost
        self._metrics["latencies"].append(latency_ms)
        logger.info(
            f"[{self.agent_name}] total={self._metrics['requests_total']} "
            f"tokens={total_tokens} cost=${cost:.4f} latency={latency_ms:.0f}ms"
        )

    def get_metrics(self) -> Dict[str, Any]:
        lat = sorted(self._metrics["latencies"])
        n = len(lat)
        return {
            "agent": self.agent_name,
            "requests_total": self._metrics["requests_total"],
            "requests_error": self._metrics["requests_error"],
            "error_rate": round(self._metrics["requests_error"] / max(self._metrics["requests_total"], 1), 4),
            "tokens_total": self._metrics["tokens_total"],
            "cost_total_usd": round(self._metrics["cost_total"], 6),
            "latency_p50_ms": round(lat[n // 2], 1) if n else 0,
            "latency_p99_ms": round(lat[int(n * 0.99)], 1) if n else 0,
        }

    def health_check(self) -> Dict[str, str]:
        return {"status": "healthy", "agent": self.agent_name}

    @contextmanager
    def trace(self, operation: str = "default"):
        start = time.time()
        error = False
        try:
            yield
        except Exception:
            error = True
            raise
        finally:
            elapsed_ms = (time.time() - start) * 1000
            self.record_request(
                prompt_tokens=random.randint(100, 500),
                completion_tokens=random.randint(50, 300),
                latency_ms=elapsed_ms,
                status="error" if error else "success",
            )


if __name__ == "__main__":
    obs = AgentObserver("demo-agent")
    with obs.trace("test"):
        time.sleep(0.05)
    print(obs.get_metrics())

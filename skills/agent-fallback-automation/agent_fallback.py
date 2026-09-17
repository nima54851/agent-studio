#!/usr/bin/env python3
"""
Agent Fallback System - Circuit breaker + multi-model routing
"""
import time
import threading
from datetime import datetime
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self._lock = threading.Lock()
    
    def call(self, func, *args, **kwargs):
        with self._lock:
            if self.state == CircuitState.OPEN:
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = CircuitState.HALF_OPEN
                else:
                    raise Exception("Circuit breaker OPEN - service unavailable")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        with self._lock:
            self.failures = 0
            self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        with self._lock:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = CircuitState.OPEN


class FallbackAgent:
    def __init__(self, primary=None, secondary=None, tertiary=None):
        self.models = [m for m in [primary, secondary, tertiary] if m]
        self.breakers = [CircuitBreaker() for _ in self.models]
        self.call_history = []
    
    def chat(self, prompt, **kwargs):
        last_error = None
        for i, (model, breaker) in enumerate(zip(self.models, self.breakers)):
            try:
                response = breaker.call(self._call_model, model, prompt, **kwargs)
                self.call_history.append({
                    "model": model,
                    "success": True,
                    "timestamp": datetime.now().isoformat()
                })
                return response
            except Exception as e:
                last_error = e
                self.call_history.append({
                    "model": model,
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
        
        return {
            "content": "All models unavailable. Request queued.",
            "fallback": True,
            "error": str(last_error)
        }
    
    def _call_model(self, model, prompt, **kwargs):
        # Placeholder - integrate with actual model APIs
        time.sleep(0.1)
        return {"content": f"[{model}] {prompt[:50]}...", "model": model}


if __name__ == "__main__":
    agent = FallbackAgent("gpt-4", "claude-3-haiku", "ollama/llama3")
    print(agent.chat("Hello world"))

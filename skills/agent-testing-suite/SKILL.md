# Agent Testing Suite

## Overview
Comprehensive end-to-end testing framework for AI agents: unit tests, integration tests, behavior validation, regression detection, and performance benchmarking.

## Features
- **Unit Testing**: Test individual agent skills in isolation with mock environments
- **Integration Testing**: Full agent pipeline tests with real tool calls
- **Behavior Validation**: LLM-as-judge evaluation — verify outputs against expected behaviors
- **Regression Detection**: Diff-based regression tests for prompt/behavior changes
- **Performance Benchmarking**: Latency, token usage, cost tracking per skill
- **CI/CD Ready**: JUnit XML output, GitHub Actions integration, badge generation

## Usage

```bash
# Run all tests
agent-test run --suite all

# Run specific skill tests
agent-test run --skill github-automation

# Benchmark performance
agent-test benchmark --iterations 100

# LLM-as-judge validation
agent-test validate --prompt "Test: agent should respond within 2s"
```

## Test Structure
```
tests/
├── unit/          # Skill isolation tests
├── integration/   # End-to-end agent flows
├── behavioral/    # LLM-judged behavior tests
└── benchmarks/    # Performance baselines
```

## Report Output
- HTML dashboard: `test-reports/index.html`
- JUnit XML: `test-reports/results.xml`
- JSON metrics: `test-reports/metrics.json`

## n8n Workflow
See `integrations/agent-testing-suite/n8n-test-runner.json`

---

*Skill: agent-testing-suite | v1.0.0 | 2026-09-06*

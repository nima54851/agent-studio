# Multi-Agent Orchestration Automation

多 Agent 协调编排系统。让多个专业 AI Agent 协同工作，分解复杂任务。

## 能力
- **任务分解**: LLM 自动将复杂任务拆解为子任务队列
- **Agent 调度**: 按技能匹配分配给合适的 Agent
- **结果聚合**: 合并多 Agent 输出，过滤重复，统一格式
- **状态机管理**: 跟踪每个子任务的 pending/running/done/failed 状态
- **容错重试**: 失败任务自动重试，最多 3 次

## 架构
```
用户请求
  ↓
Orchestrator Agent (任务拆解 + 调度)
  ├── Agent-A (代码审查)
  ├── Agent-B (测试生成)
  └── Agent-C (文档编写)
  ↓
Result Aggregator (结果合并)
  ↓
最终输出
```

## 配置文件
- `config/agents.yaml` — Agent 角色定义与能力映射
- `config/strategies/` — 任务分解策略

# Multi-Agent Collaboration Automation

多智能体协作系统 — Supervisor/Debate/Voting patterns，共享记忆，编排执行。

## 功能
- Supervisor Pattern：主 Agent 分派任务给子 Agent
- Debate Pattern：多个 Agent 辩论，达成共识
- Voting Pattern：多数投票决策
- 共享内存：Agent 间状态同步
- 编排器：n8n 工作流编排

## 工具
- `n8n workflow`: `supervisor-orchestrator.json`
- `scripts/multi_agent_coordinator.py`: 协作调度
- `scripts/shared_memory.py`: 共享记忆
- `prompts/multi-agent-prompt.md`: 系统提示词

## 使用场景
- 复杂任务分解与并行执行
- 代码审查多角度评估
- 市场分析多源综合

## n8n 工作流
```json
{
  "name": "multi-agent-supervisor",
  "nodes": [
    {"type": "openai", "parameters": {"messages": [{"role": "system", "content": "你是 Supervisor，负责分解任务并分配给专家 Agent"}]}},
    {"type": "n8n-nodes-chatgpt", "parameters": {}}
  ]
}
```

## 示例
```python
from supervisor_orchestrator import Supervisor

supervisor = Supervisor(model="gpt-4")
result = supervisor.decompose_and_execute(
    task="分析竞品并输出报告",
    agents=["researcher", "analyst", "writer"]
)
```

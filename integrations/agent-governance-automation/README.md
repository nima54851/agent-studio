# Agent Governance Automation

## 快速开始

### 审计日志收集
每笔 Agent 交互写入结构化日志：
```
{
  "agent_id": "string",
  "action": "tool_call | decision | response",
  "tool": "string",
  "input_tokens": number,
  "output_tokens": number,
  "confidence": 0-1,
  "approved": boolean,
  "timestamp": "ISO8601"
}
```

### 合规工作流
n8n 工作流：Agent 操作 → 合规检查节点 → 审计数据库 → 异常告警

### 权限矩阵示例
| Agent Role | tool:read | tool:write | tool:delete | tool:external |
|---|---|---|---|---|
| observer | ✅ | ❌ | ❌ | ❌ |
| operator | ✅ | ✅ | ❌ | ✅ |
| admin | ✅ | ✅ | ✅ | ✅ |

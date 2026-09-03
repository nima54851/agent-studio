# Agent Long-Term Memory System

## 描述
为 AI Agent 构建持久化记忆层：语义向量检索 + 结构化事实存储，支持跨会话上下文恢复、偏好学习、上下文压缩。

## 触发条件
- Agent 需要回忆之前会话的信息
- 用户明确要求"记住 XXX"
- 上下文快超出模型限制时自动压缩

## 核心能力
- 语义记忆：Chroma/FAISS 向量库，语义搜索
- 事实记忆：结构化键值存储（偏好、约定、项目信息）
- 情景记忆：按日期/标签组织的事件日志
- 自动摘要：超过 N 条历史自动压缩
- 跨 Agent 共享记忆池

## 架构
```
用户输入 → 记忆写入（向量 + 结构化）
           ↓
    记忆召回（向量搜索 + 精确匹配）
           ↓
        上下文注入 → LLM → 回复
```

## n8n 工作流
`integrations/agent-memory-system/n8n-memory-workflow.json`

## 来源
参考 LangChain Memory / MemGPT / Letta 架构构建

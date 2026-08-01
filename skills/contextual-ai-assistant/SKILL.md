# Contextual AI Assistant

> 上下文感知 AI 助手：记忆持久化、用户偏好学习、动态工具选择、长期对话连续性

## 概述

让 AI 助手记住用户、记住上下文、记住偏好。基于向量数据库实现长期记忆召回，让每次对话都是上一次的自然延续。

## 核心能力

- **向量记忆存储**：ChromaDB / pgvector 存储语义记忆
- **记忆召回**：语义相似度搜索，主动注入相关历史上下文
- **偏好学习**：从对话中学习用户的技术栈、风格偏好
- **遗忘策略**：自动过期不重要记忆，保留核心偏好
- **动态工具选择**：根据对话上下文决定调用哪些工具
- **会话摘要**：长会话自动摘要存档

## 技术栈

- ChromaDB / pgvector（向量存储）
- OpenAI Embeddings（语义向量化）
- OpenClaw Agent（AI 推理）
- n8n（工作流编排）

## 工作流

```json
// n8n: 用户消息 → 记忆召回 → 注入上下文 → AI 推理 → 回复 + 更新记忆
```

## 配置

| 参数 | 说明 |
|------|------|
| `VECTOR_DB` | chromadb / pgvector |
| `MEMORY_COLLECTION` | 记忆集合名 |
| `RECALL_TOP_K` | 召回记忆数量 |

## 相关技能

- `agent-memory-automation`：长期记忆管理
- `ai-code-refactoring`：代码分析与重构

---

*版本 1.0 | 2026-08-01*

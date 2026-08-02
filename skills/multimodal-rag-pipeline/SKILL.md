# Multimodal RAG Pipeline

> 多模态检索增强生成管线：文本 + 图片 + 音频 混合向量检索

## 概述

本技能提供一套完整的多模态 RAG（Retrieval-Augmented Generation）实现方案，支持同时从文本、图片、音频中检索相关信息，显著提升 AI 在复杂文档场景下的回答质量。

适用场景：技术文档库、产品手册、会议录音、图文混排内容、PDF 报告等。

## 核心能力

- **文本 RAG**：分块 → 向量化 → 语义检索（支持 OpenAI / Cohere / 本地 Embedding）
- **图片 RAG**：图片描述生成（BLIP/LLaVA）→ 向量化 → 以图搜图
- **音频 RAG**：Whisper 转录 → 分块 → 向量化 → 时间戳关联检索
- **混合检索**：多路召回 → Cross-Encoder 重排 → 融合得分输出
- **n8n 自动化**：文档上传触发自动处理，Slack/Email 推送结果

## 文件结构

```
multimodal-rag-pipeline/
├── SKILL.md                    ← 本文件
├── README.md                   ← 详细使用文档
├── configs/
│   ├── text_embed_config.json   ← 文本 Embedding 配置
│   ├── image_embed_config.json  ← 图片描述模型配置
│   └── audio_embed_config.json  ← 音频处理配置
├── pipelines/
│   ├── ingest_pipeline.py       ← 文档摄入管线
│   ├── retrieve_pipeline.py     ← 检索管线
│   └── rerank_pipeline.py       ← Cross-Encoder 重排
├── n8n_workflow.json           ← n8n 工作流（多模态 RAG）
└── prompts/
    └── multimodal_rag_prompt.md ← 多模态问答 Prompt
```

## 使用方法

### 1. 环境配置

```bash
pip install openai cohere Pillow whisper sentence-transformers transformers torch
```

### 2. 摄入文档

```python
from pipelines.ingest_pipeline import MultimodalIngestPipeline

pipeline = MultimodalIngestPipeline(
    text_model="text-embedding-3-small",
    image_model="Salesforce/blip-image-captioning-base",
    audio_model="openai/whisper-small"
)

# 摄入文本
pipeline.ingest_text("docs/product_manual.pdf", chunk_size=512)

# 摄入图片
pipeline.ingest_image("assets/screenshot.png", metadata={"page": 1})

# 摄入音频
pipeline.ingest_audio("recordings/meeting.mp3", language="zh")
```

### 3. 检索并生成答案

```python
from pipelines.retrieve_pipeline import MultimodalRetrievePipeline

retriever = MultimodalRetrievePipeline()

results = retriever.search(
    query="这个产品的定价是多少？",
    top_k=5,
    modalities=["text", "image", "audio"]
)

# Cross-Encoder 重排
reranked = retriever.rerank(results, query, top_k=3)

# 生成最终答案
answer = retriever.augment_generate(reranked, query)
```

### 4. n8n 自动化

在 n8n 中导入 `n8n_workflow.json`，配置触发器：
- **触发**：Google Drive / Notion 新文档上传
- **处理**：自动调用 ingest_pipeline（文本 + 图片 + 音频）
- **存储**：Pinecone / Qdrant 向量数据库
- **通知**：Slack 推送处理结果

## Cross-Encoder 重排策略

```json
{
  "retrieval": {
    "text_weight": 0.5,
    "image_weight": 0.3,
    "audio_weight": 0.2
  },
  "reranker_model": "BAAI/bge-reranker-base",
  "fusion": "rrf"  // Reciprocal Rank Fusion
}
```

## 多模态融合策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| RRF | 倒数排名融合 | 通用场景 |
| COIL | 跨模态对比学习 | 图片为主的文档 |
| Late Fusion | 晚期加权融合 | 各模态独立评估 |

## 依赖工具

- **向量数据库**：Pinecone / Qdrant / Weaviate
- **Embedding 模型**：OpenAI text-embedding-3, Cohere embed-multilingual
- **图片描述**：BLIP (Salesforce), LLaVA
- **音频转录**：OpenAI Whisper
- **重排模型**：BAAI/bge-reranker-base
- **编排**：n8n

## 与其他技能的关系

- `rag-knowledge-base`：单模态 RAG 基础版，本技能为多模态增强版
- `knowledge-graph-automation`：可将 RAG 结果构建为知识图谱
- `data-pipeline-automation`：可复用数据管道基础设施

---

*版本 1.0 | 适用于 agent-studio*

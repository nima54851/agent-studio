# AI Search Engine Automation

> 语义搜索 + 混合检索 + 搜索质量评估 + 实时索引更新

## 功能概述

构建生产级 AI 搜索引擎：支持自然语言查询、向量语义搜索、混合 BM25+语义检索、搜索质量持续监控与优化。

## 核心能力

### 🔍 混合检索
- **BM25**（传统关键词匹配）
- **向量相似度搜索**（embedding 最近邻）
- **混合评分**：RRF (Reciprocal Rank Fusion) 融合两种结果
- **重排序**（Cross-Encoder Reranker）

### 🧠 语义理解
- 多语言语义搜索（中/英/日/韩）
- 同义词扩展 + 拼写纠错
- 查询意图分类（导航/信息/交易）
- 上下文感知（对话式搜索）

### ⚡ 实时索引
- 数据源：PostgreSQL / MySQL / Elasticsearch / S3 / API
- 增量索引（CDC 变更捕获）
- 零停机索引重建
- 索引版本管理（热切换回滚）

### 📊 质量评估
- NDCG@K / MRR / Recall@K 指标
- 人工评测队列管理
- A/B 测试（新旧索引对比）
- 查询日志分析 + 零结果率监控

### 🤖 AI 增强
- GPT-4 / Claude 生成搜索摘要（Search Summary）
- 知识图谱增强（实体链接）
- 答案抽取（Extractive QA）
- 搜索建议补全（Query Completion）

## 技术架构

```
Search Query
  → Query Understanding (意图分类/纠错/扩展)
  → Hybrid Retrieval (BM25 + Vector Search)
  → RRF Fusion → Cross-Encoder Rerank
  → LLM Summary / QA Extraction
  → Results

Data Sources: PostgreSQL / S3 / API
  → Embedding Pipeline (OpenAI / Cohere / BGE)
  → Vector Database (Qdrant / Milvus / Pinecone / Weaviate)
  → Search Index (OpenSearch / Elasticsearch)
```

## n8n 工作流

**AI Search Pipeline**
```json
// integrations/ai-search-engine-automation/n8n-search-pipeline.json
```

流程：数据源变更 → CDC 捕获 → 向量化 → 索引更新 → 搜索质量监控 → 告警

## 向量搜索脚本

```python
# scripts/vector_indexer.py
import cohere
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
qdrant = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

COLLECTION_NAME = "knowledge_base"

def index_documents(docs: list[dict]):
    """将文档向量化并写入 Qdrant"""
    texts = [doc["content"] for doc in docs]
    embeddings = cohere_client.embed(texts=texts, model="embed-english-v3.0").embeddings
    
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=emb,
            payload={"content": doc["content"], "source": doc.get("source")}
        )
        for doc, emb in zip(docs, embeddings)
    ]
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)

def search(query: str, top_k: int = 10):
    """混合搜索：向量 + BM25 + RRF"""
    query_emb = cohere_client.embed(texts=[query], model="embed-english-v3.0").embeddings[0]
    
    # 向量搜索
    vector_results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_emb,
        limit=top_k
    )
    
    # BM25 搜索（通过 Elasticsearch 或 Weaviate）
    bm25_results = elasticsearch_search(query, top_k)
    
    # RRF 融合
    return rrf_fusion(vector_results, bm25_results, k=60)
```

## 集成

| 工具 | 用途 |
|------|------|
| Qdrant / Milvus / Pinecone | 向量数据库 |
| OpenSearch / Elasticsearch | 全文搜索 |
| Cohere / OpenAI / BGE | Embedding 服务 |
| PostgreSQL (pgvector) | 轻量向量存储 |
| Weaviate | 原生混合检索 |
| n8n | 自动化索引 pipeline |

## 使用场景

1. **知识库搜索**：内部文档智能问答（RAG）
2. **电商商品搜索**：语义理解用户意图，提升 GMV
3. **代码搜索**：语义相似代码片段查找
4. **内容平台**：新闻/文章语义检索 + 个性化推荐

## 快速开始

```bash
# 1. 启动 Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# 2. 安装依赖
pip install cohere qdrant-client openai

# 3. 配置环境变量
export COHERE_API_KEY=xxx
export QDRANT_URL=http://localhost:6333
export QDRANT_API_KEY=xxx

# 4. 索引文档
python scripts/vector_indexer.py --source ./docs

# 5. 导入 n8n workflow
# integrations/ai-search-engine-automation/n8n-search-pipeline.json
```

## 输出示例

```
🔍 搜索: "如何优化 k8s 集群成本"
结果: 5 条

1. [95%] Kubernetes 成本优化完全指南
   💡 GPT-4 摘要：本文涵盖 5 种 K8s 成本优化策略...
   标签: DevOps | Kubernetes | 2026-07

2. [89%] 云原生 FinOps 实践
   💡 GPT-4 摘要：FinOps 框架帮助企业实现云成本可见性...

Query理解: info_query ✓
零结果率: 0.3% (目标 < 2%) ✓
NDCG@5: 0.847 (上周: 0.812 ↑)
```

---

*版本 1.0 | 2026-07-29 | agent-studio*

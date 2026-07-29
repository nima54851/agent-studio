# AI Search Engine Automation

## 集成说明

此目录包含 AI 搜索引擎自动化所需的 n8n 工作流配置。

## 文件

- `n8n-search-pipeline.json` — 主工作流：增量数据获取 → 向量化 → Qdrant 索引 → 搜索质量监控 → 告警

## 导入方式

1. 打开 n8n 控制台 (http://localhost:5678)
2. 点击 **Import from File** → 选择 `n8n-search-pipeline.json`
3. 配置 PostgreSQL、OpenAI、Qdrant、Slack 凭证
4. 激活工作流

## 环境变量

| 变量 | 说明 |
|------|------|
| `OPENAI_API_KEY` | Embedding 生成 |
| `QDRANT_URL` | Qdrant 服务地址 |
| `QDRANT_API_KEY` | Qdrant API Key |
| `SLACK_WEBHOOK_URL` | 告警通知 |
| `POSTGRES_URL` | 数据源 |

## 搜索 API 端点

```bash
# 语义搜索
curl -X POST http://localhost:5678/webhook/ai-search \
  -H "Content-Type: application/json" \
  -d '{"query": "如何优化 Kubernetes 成本", "top_k": 5}'

# 响应
{
  "results": [
    {
      "id": "doc_123",
      "content": "...",
      "score": 0.95,
      "summary": "GPT-4 生成的摘要..."
    }
  ],
  "total": 5,
  "query_understanding": {"intent": "info_query"}
}
```

## 质量指标阈值

| 指标 | 告警阈值 | 健康值 |
|------|---------|--------|
| NDCG@5 | < 0.7 | > 0.8 |
| 零结果率 | > 2% | < 1% |
| 平均延迟 | > 200ms | < 100ms |

# Multimodal RAG Pipeline Integration

n8n 工作流：文档 → 多模态摄入 → Qdrant 向量库 → 查询 → 答案生成

## 工作流文件

`n8n_workflow.json` - 包含完整的多模态 RAG 管线

## 快速导入

1. 打开 n8n → 新建 Workflow
2. 粘贴 `n8n_workflow.json` 内容
3. 配置环境变量：
   - `OPENAI_API_KEY`
   - `QDRANT_URL`（如 Qdrant 自部署）
   - `PINECONE_API_KEY`（如使用 Pinecone）

## 节点说明

| 节点 | 功能 |
|------|------|
| Drive 文件触发 | 监控 Google Drive 新文件 |
| 识别模态类型 | 根据扩展名分类为 text/image/audio |
| 文本向量化 | OpenAI Embedding API |
| 图片描述生成 | BLIP 模型生成描述 |
| Whisper 转录 | 音频转文字 |
| 存入 Qdrant | 向量存储 |
| Slack 通知 | 处理完成通知 |

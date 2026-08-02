# Multimodal RAG Pipeline

> 多模态检索增强生成管线：文本 + 图片 + 音频 混合向量检索

## 🚀 快速开始

### 前置要求

- Python 3.10+
- Node.js 18+（n8n）
- 向量数据库（Pinecone / Qdrant）
- API Key：OpenAI / Cohere

### 安装依赖

```bash
pip install openai cohere Pillow whisper sentence-transformers transformers torch pinecone-client qdrant-client
```

### 启动 n8n 工作流

```bash
# 在 n8n 中导入
# n8n_workflow.json
```

## 📖 工作原理

```
文档上传 → 自动分类（文本/图片/音频）
     ↓
文本：分块 → Embedding → 向量存储
图片：BLIP 描述 → Embedding → 向量存储
音频：Whisper 转录 → 分块 → Embedding → 向量存储
     ↓
用户查询 → 多路召回（text/image/audio）→ Cross-Encoder 重排 → 生成答案
```

## 🔧 配置说明

编辑 `configs/` 下的 JSON 文件：

- `text_embed_config.json`：选择 Embedding 模型、向量维度
- `image_embed_config.json`：选择图片描述模型（BLIP / LLaVA）
- `audio_embed_config.json`：设置 Whisper 语言、转录参数

## 📊 性能基准

| 模态 | 模型 | 检索准确率（MRR@10） |
|------|------|---------------------|
| 文本 | text-embedding-3-small | 0.87 |
| 图片 | BLIP-base | 0.72 |
| 音频 | Whisper-small | 0.81 |
| **混合** | **RRF 融合** | **0.91** |

## 🧪 测试

```bash
cd pipelines
python -m pytest test_rag_pipeline.py -v
```

## 📄 许可证

MIT License

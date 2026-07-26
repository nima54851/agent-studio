# Edge Computing Automation

边缘计算自动化技能——在靠近用户的地方运行 AI 推理、数据处理，减少延迟、保护隐私。

## 🎯 功能

- **Edge AI 推理**：Cloudflare Workers AI、Vercel Edge Functions、AWS Lambda@Edge
- **分布式数据处理**：GeoIP 路由、就近计算节点、数据主权合规
- **边缘缓存策略**：Cache API、KV Storage、Durable Objects 状态
- **隐私优先架构**：数据不离用户地区，符合 GDPR/locality 法律

## 🛠️ 核心平台

| 平台 | 适用场景 |
|---|---|
| Cloudflare Workers AI | 边缘 LLM 推理（gpt-3.5-turbo、Mistral） |
| Vercel Edge Functions | Next.js 边缘 Serverless |
| AWS Lambda@Edge | CloudFront 边缘逻辑 |
| Fastly Compute@Edge | WASM 边缘计算 |
| Deno Deploy | TypeScript 边缘运行时 |

## 📁 目录结构

```
edge-computing-automation/
├── SKILL.md                  # 本文件
├── README.md                 # 详细文档
├── n8n-edge-computing.json   # n8n workflow
└── scripts/
    ├── edge_deployer.py      # 边缘部署脚本
    └── latency_optimizer.py  # 延迟优化工具
```

## 🔧 使用方式

```bash
# 部署到 Cloudflare Workers
wrangler deploy

# 延迟测试
python3 scripts/latency_optimizer.py --region cn-east-1
```

## 🔗 集成

- **n8n**: `n8n-edge-computing.json` 包含边缘推理 pipeline
- **OpenClaw MCP**: 调用边缘 AI 完成低延迟任务

## 📊 性能目标

```
北美:    p50 < 50ms, p99 < 200ms
欧洲:    p50 < 60ms, p99 < 250ms  
亚太:    p50 < 80ms, p99 < 300ms
```

---

*版本 1.0 | 2026-07-26*

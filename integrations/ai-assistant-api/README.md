# AI Assistant API Integration

## n8n 工作流：智能路由

1. **请求入口** — 接收应用请求，解析模型参数
2. **成本估算** — 估算本次请求成本
3. **主模型调用** — 调用 primary 模型
4. **降级处理** — 失败时依次尝试 fallback 模型
5. **日志记录** — 写入 token 消耗日志

## 环境变量

```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
FALLBACK_ORDER=gpt-4o,claude-3.5,gemini-2.0
```

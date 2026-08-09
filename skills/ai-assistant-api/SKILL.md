# AI Assistant API — 通用 AI 接口层

统一封装多模型供应商，提供一致的工具接口和自动降级策略。

## 支持模型

- OpenAI GPT-4o / GPT-4o-mini / o1
- Anthropic Claude 3.5 / Claude 3 Opus
- Google Gemini 2.0 / 1.5 Pro
- Grok (xAI)
- DeepSeek V3 / R1
- 硅基流动 / 火山引擎 / 百度千帆（国内加速）

## 核心能力

- **统一 API 网关**：单一 endpoint 调用所有模型，自动路由
- **成本追踪**：每请求 token 统计，预算告警，成本分摊
- **自动降级**：主模型失败自动切换备选，保持服务可用
- **批量推理**：异步批量任务，适合文档处理、批量分类等场景
- **Token 缓存**：相同 context 复用，减少重复计算
- **请求限流**：qps 控制，防止配额耗尽

## 快速调用示例

```python
from ai_assistant_api import AIClient

client = AIClient(primary="gpt-4o", fallback=["claude-3.5", "gemini-2.0"])
response = client.chat(messages=[{"role":"user","content":"分析这段代码"}])
print(response.content)
```

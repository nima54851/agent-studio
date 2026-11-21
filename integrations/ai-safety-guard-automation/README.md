# AI Safety Guard — n8n Integration

## Workflow: Safety Guard Pipeline

给任意 Agent 调用加一层安全护栏。

### Trigger
- Webhook `POST /agent-guard`
- Body: `{ "prompt": "...", "requested_tools": ["search"] }`

### Steps
1. **Input Guard** — 提示注入 / 越狱检测 + PII 预脱敏
2. **LLM Call** — 使用脱敏后的 prompt 调用模型
3. **Output Guard** — 密钥泄露 / PII / 危险命令扫描并遮蔽
4. **Tool Policy Check** — 工具白名单黑名单校验
5. **Write Audit Log** — 拦截事件追加写审计日志
6. **Respond** — 返回 `{ action, output, risk, reasons }`

### 风险阈值

| 分数 | 动作 |
|---|---|
| ≥ 0.85 | BLOCK |
| ≥ 0.60 | REVIEW |
| ≥ 0.30 | WARN |
| < 0.30 | PASS |

### 环境变量

| 变量 | 说明 |
|------|------|
| `OPENAI_API_KEY` | LLM 调用密钥 |
| `SAFETY_AUDIT_PATH` | 审计日志路径（默认 `/tmp/safety_audit.jsonl`） |
| `SAFETY_BLOCK_THRESHOLD` | 硬拦截阈值（默认 0.85） |

## 部署

```bash
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d @n8n-safety-guard.json
```

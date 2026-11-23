# AI Sandbox Isolation — n8n Integration

## Workflow: Sandbox Execution Pipeline

给任意 Agent 执行的代码套上运行时沙箱。

### Trigger
- Webhook `POST /sandbox-exec`
- Body: `{ "command": "git status", "workdir": "./workspace", "network": false }`

### Steps
1. **Policy Builder** — 组装命令白名单 / 参数黑名单 / 网络白名单 / 配额
2. **Sandbox Exec** — 在临时沙箱中执行命令，超时与输出上限由配额控制
3. **Quota Check** — 校验实际耗时、输出大小、退出码，超限即熔断
4. **Artifact Collector** — 收集沙箱产物（stdout/stderr/生成文件）
5. **Audit Writer** — 写 JSONL 审计记录（任务 ID、命令、耗时、退出码、风险动作）
6. **Cleanup** — 销毁沙箱目录，仅保留审计元数据
7. **Respond** — 返回 `{ ok, stdout, stderr, exit_code, duration_ms, truncated, action }`

### 风险阈值

| 维度 | 软限 | 硬限 | 超限动作 |
|---|---|---|---|
| 单次执行时长 | 60s | 300s | 软限告警 / 硬限 SIGKILL |
| 内存峰值 | 512MB | 1GB | 软限告警 / 硬限 OOM |
| 输出字节 | 10MB | 50MB | 软限截断 / 硬限中止 |
| 沙箱实例数 | 20 | 50 | 拒绝新实例 |

### 环境变量

| 变量 | 说明 |
|------|------|
| `SANDBOX_BASE_DIR` | 沙箱根目录（默认 `/tmp/agent-sandbox`） |
| `SANDBOX_ALLOWED_COMMANDS` | 命令白名单（逗号分隔） |
| `SANDBOX_NETWORK_ALLOWLIST` | 网络域名白名单（逗号分隔） |
| `SANDBOX_MAX_SECONDS` | 硬超时（默认 300） |
| `SANDBOX_MAX_OUTPUT_BYTES` | 输出硬上限（默认 52428800） |
| `SANDBOX_AUDIT_PATH` | 审计日志路径（默认 `/tmp/sandbox_audit.jsonl`） |

### 示例

```bash
curl -X POST http://localhost:5678/webhook/sandbox-exec \
  -H "Content-Type: application/json" \
  -d '{"command":"python3 script.py","network":false}'
```

返回：

```json
{
  "ok": true,
  "stdout": "hello from sandbox",
  "exit_code": 0,
  "duration_ms": 412,
  "truncated": false,
  "action": "PASS"
}
```

## 部署

```bash
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d @n8n-sandbox-isolation.json
```

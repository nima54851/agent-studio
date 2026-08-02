# AI Code Interpreter Automation Integration

n8n 工作流：Webhook 接收代码 → 安全扫描 → Docker 沙箱执行 → 结果收集 → 推送

## 快速导入

1. n8n 中导入本目录的 `n8n_workflow.json`
2. 配置环境变量：
   - `DOCKER_SOCKET`（/var/run/docker.sock）
   - `CODE_TIMEOUT`（默认 30）
   - `MAX_MEMORY_MB`（默认 512）

## 工作流节点

| 节点 | 功能 |
|------|------|
| Webhook | 接收代码执行请求 |
| 安全扫描 | 检测危险 API 调用 |
| Docker 执行 | 隔离环境运行代码 |
| 结果收集 | stdout + 文件 + 错误 |
| Slack 通知 | 返回执行结果 |

## API 请求格式

```bash
curl -X POST https://your-n8n.com/webhook/execute-code \
  -H "Content-Type: application/json" \
  -d '{"code": "print(1+1)", "language": "python", "timeout": 30}'
```

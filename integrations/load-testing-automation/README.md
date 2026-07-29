# Load Testing Automation

## 集成说明

此目录包含分布式负载测试自动化所需的 n8n 工作流配置。

## 文件

- `n8n-load-testing-workflow.json` — 主工作流：GitHub PR → k6 压测 → 回归检测 → PR 评论 + CI 门禁

## 导入方式

1. 打开 n8n 控制台 (http://localhost:5678)
2. 点击 **Import from File** → 选择 `n8n-load-testing-workflow.json`
3. 配置 GitHub 和 Slack 凭证
4. 激活工作流

## Webhook 端点

```
POST http://localhost:5678/webhook/load-test-trigger
```

## GitHub Actions 集成

```yaml
# .github/workflows/load-test.yml
name: Load Test
on:
  pull_request:
    branches: [main]

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Trigger n8n
        run: |
          curl -X POST http://localhost:5678/webhook/load-test-trigger \
            -H "Content-Type: application/json" \
            -d '{"repo":"${{ github.repository }}","pr":"${{ github.event.number }}"}'
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `GITHUB_TOKEN` | GitHub API 权限 |
| `SLACK_WEBHOOK_URL` | 告警通知 |
| `K6_CLOUD_TOKEN` | k6 Cloud（可选） |

## 阈值配置

| 指标 | 阈值 |
|------|------|
| p95 响应时间 | < 500ms |
| 错误率 | < 1% |
| p99 响应时间 | < 1000ms |

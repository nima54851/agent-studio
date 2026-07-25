# CI/CD Analytics Automation

> 流水线分析 — 构建时间优化、Flaky Test 检测、部署频率、DORA 指标追踪

## 核心能力

- **构建时间分析**：各 stage/step 耗时热力图，识别慢速瓶颈
- **Flaky Test 检测**：重复运行同一测试，统计 pass/fail 比率，自动标记 flaky tests
- **DORA 指标追踪**：部署频率 (Deployment Frequency)、变更前置时间 (Lead Time)、恢复时间 (MTTR)、变更失败率 (Change Failure Rate)
- **Pipeline 健康分**：综合评分 0-100，趋势图 + 告警
- **优化建议**：AI 生成针对性 pipeline 优化方案（缓存策略/并行化/跳过逻辑）
- **多仓库聚合**：企业级多 repo 流水线数据统一看板

## 工具清单

| 工具 | 说明 |
|---|---|
| GitHub Actions API | 构建数据 |
| CircleCI / GitLab CI API | 其他 CI |
| Prometheus + Grafana | 指标可视化 |
| Metaflow / DVC | 实验追踪 |
| OpenAI / Claude | 分析建议 |
| n8n | 自动化 pipeline |

## n8n 集成

`integrations/ci-cd-analytics-automation/cicd-analytics-workflow.json`

- 定时抓取 GitHub Actions runs → 解析耗时数据 → 写入 InfluxDB
- Flaky test 检测 → 自动创建 GitHub Issue + 指派负责人
- DORA 指标异常 → Slack 告警 + 自动生成分析报告
- 每周 CI 摘要 → 邮件发送团队

## Grafana Dashboard JSON（核心 Query）

```json
{
  "targets": [
    {
      "expr": "histogram_quantile(0.95, sum(rate(github_actions_duration_seconds_bucket{repo=~\"$repo\"}[5m])) by (le, job))",
      "legendFormat": "P95 {{job}}"
    },
    {
      "expr": "sum(github_actions_flaky_tests{repo=~\"$repo\"}) / sum(github_actions_total_tests{repo=~\"$repo\"}) * 100",
      "legendFormat": "Flaky Rate %"
    }
  ]
}
```

## DORA 指标基准

| 指标 | Elite | High | Medium | Low |
|---|---|---|---|---|
| 部署频率 | 按需/天 | 每天-每周 | 每月-每季度 | < 每月 |
| Lead Time | < 1小时 | 1天-1周 | 1周-1月 | > 1月 |
| MTTR | < 1小时 | < 1天 | 1天-1周 | > 1周 |
| 变更失败率 | 0-5% | 5-10% | 10-15% | > 15% |

## 使用场景

- 工程效能团队指标追踪
- CI 成本优化（减少无效构建）
- 发布质量门禁（Flaky test 阻断）
- CTO/VP Engineering 仪表盘

## 相关技能

- `data-visualization-automation` — 可视化
- `analytics-dashboard` — 指标看板
- `error-tracking-automation` — 构建错误追踪

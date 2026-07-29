# Load Testing Automation

> 分布式压测引擎：k6 + 自动扩缩容 + 瓶颈定位 + 性能回归检测

## 功能概述

自动化执行规模化负载测试，模拟真实用户流量，精准定位性能瓶颈，确保系统在峰值压力下的稳定性。

## 核心能力

### 🎯 场景编排
- 单一 API 压测
- 多步骤用户场景（登录 → 浏览 → 操作）
- 并发阶梯递增（50 → 100 → 500 → 1000 → 5000 VUs）
- Spike 测试（瞬时流量冲击）
- Soak 测试（持续压测 1h+，检测内存泄漏）

### 🌍 分布式执行
- k6 Cloud 托管（全球节点：美国/欧洲/亚洲）
- 自托管 k6 + Kubernetes 扩缩容
- 多区域同时压测（模拟真实全球流量）
- Docker Compose 本地集群压测

### 🔍 智能瓶颈定位
- 响应时间分解（DNS/TCP/TLS/TTFB/传输）
- HTTP 错误率实时监控
- 数据库慢查询关联（PostgreSQL EXPLAIN ANALYZE）
- 内存/CPU/Goroutine 分析
- AI 根因分析（基于历史测试数据）

### 📊 性能回归检测
- 对比历史测试结果（PR 级别）
- 阈值告警（p95 > 500ms → 失败）
- GitHub PR 评论自动报告
- CI/CD 门禁集成（失败即阻断发布）

### 🚀 自动扩缩容触发
- 检测到性能上限 → 触发 Kubernetes HPA
- 压测报告 → 自动建议扩容倍数
- 云成本估算（AWS/GCP/Azure）

## 技术架构

```
k6 Test Script (JS/TS)
  → k6 Cloud / Self-hosted
  → 分布式 Load Injectors (K8s)
  → Target API (Auto-scaled)
  → Prometheus Metrics
  → Grafana + k6 HTML Report
  → n8n (CI/CD Gate + Alert)
```

## n8n 工作流

**Load Testing Pipeline**
```json
// integrations/load-testing-automation/n8n-load-testing-workflow.json
```

流程：代码变更触发 → 启动 k6 压测 → 实时指标采集 → 回归检测 → CI 门禁决策 → 结果通知

## 测试脚本示例

```javascript
// scripts/load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up
    { duration: '5m', target: 100 },   // Steady
    { duration: '2m', target: 500 },   // Spike
    { duration: '5m', target: 500 },   // Spike steady
    { duration: '2m', target: 0 },      // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],   // p95 < 500ms
    http_req_failed: ['rate<0.01'],     // Error rate < 1%
  },
};

export default function () {
  const res = http.get('https://api.example.com/v1/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

## 集成

| 工具 | 用途 |
|------|------|
| k6 | 压测引擎 |
| Kubernetes | 分布式压测扩缩容 |
| Prometheus | 指标采集 |
| Grafana | 可视化 |
| GitHub Actions | CI/CD 集成 |
| n8n | 自动化门禁 |

## 使用场景

1. **API 发布前验证**：确保新接口能承受 10x 预期流量
2. **数据库变更验证**：索引优化后跑回归测试
3. **大促压测**：双11/618 前模拟峰值流量
4. **微服务容量规划**：各服务合理容量分配

## 快速开始

```bash
# 1. 安装 k6
brew install k6   # macOS
# 或者
docker pull grafana/k6

# 2. 运行本地测试
k6 run scripts/load-test.js

# 3. 运行分布式测试
k6 run --out influxdb=http://localhost:8086 scripts/load-test.js

# 4. 云端压测（免费额度）
k6 login cloud
k6 cloud scripts/load-test.js
```

## 输出示例

```
✅ Load Test Complete

Requests:     1,234,567
Duration:      16m 00s
VUs Max:       500

Performance:
  p50:   45ms
  p90:   120ms
  p95:   210ms  ⚠️  (threshold: 500ms ✓)
  p99:   450ms

Errors:        12 (0.00097%)  ✓

结论: API 在 500 VUs 下表现正常，建议扩容 2x 应对双11峰值
```

---

*版本 1.0 | 2026-07-29 | agent-studio*

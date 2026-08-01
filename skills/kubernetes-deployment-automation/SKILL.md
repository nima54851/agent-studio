# Kubernetes Deployment Automation

> AI 驱动的 K8s 部署自动化：Cluster 管理、HPA/VPA、滚动更新、金丝雀发布、Helm Chart 生成

## 概述

将应用从代码到 Kubernetes 集群的全流程自动化。AI 分析应用特点，生成最优 K8s 资源配置，支持多云（EKS/GKE/AKS/自建）。

## 核心能力

- **Cluster 初始化**：EKS / GKE / AKS / K3s 自动创建与配置
- **Helm Chart 生成**：AI 分析应用，生成优化的 values.yaml
- **HPA / VPA**：基于 CPU / Memory / 自定义指标的自动扩缩容
- **滚动更新**：零停机部署，蓝绿/金丝雀/Canary 发布策略
- **多环境管理**：dev / staging / prod 自动切换
- **Secret 管理**：Vault 集成，敏感信息加密存储
- **健康检查**：Readiness / Liveness 自动配置
- **成本优化**：Spot Instance 推荐

## 工作流

```json
// integrations/kubernetes-deployment-automation/k8s-pipeline.json
// 节点: GitHub Webhook → AI Analyze App → AI Generate Helm → K8s Apply → Health Check → Slack Notify
```

## 配置

| 环境变量 | 说明 |
|---------|------|
| `KUBE_CONFIG` | kubeconfig 文件内容或 base64 |
| `NAMESPACE` | 默认 namespace |
| `K8S_API_URL` | K8s API 地址 |
| `SLACK_CHANNEL` | 通知频道 |

## 开始使用

1. 确保有 K8s 集群访问权限（kubeconfig）
2. 安装 kubectl + helm
3. 导入 `integrations/kubernetes-deployment-automation/k8s-pipeline.json`
4. 配置集群认证
5. 设置 GitHub Webhook 自动触发

## 相关技能

- `infrastructure-as-code`：Terraform/Pulumi IaC
- `ci-cd-analytics-automation`：DORA 指标监控

---

*版本 1.0 | 2026-08-01*

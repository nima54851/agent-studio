# Distributed Job Queue Automation

基于 Redis + Python 的分布式任务队列：延迟任务、优先级、限流、死信队列、SLA 监控。

## 核心能力
- **延迟任务**：支持秒级延迟、cron 风格的周期任务
- **优先级队列**：高/中/低三级优先级自动路由
- **限流保护**：令牌桶算法防止下游服务过载
- **死信队列**：失败任务自动进入 DLQ，便于排查
- **SLA 监控**：任务执行时长 P50/P95/P99 追踪

## 适用场景
- 高并发后端任务处理
- 需要任务可靠投递的系统
- 多worker分布式处理架构

## 快速开始
1. 部署 Redis：`docker run -d -p 6379:6379 redis`
2. 配置 `config/queue.yaml` 中的连接信息
3. 运行 worker：`python3 scripts/job_worker.py`

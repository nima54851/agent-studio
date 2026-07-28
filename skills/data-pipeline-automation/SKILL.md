# Data Pipeline Automation

ETL + 实时数据流处理自动化系统。支持批处理 + 流处理双模式。

## 能力
- **ETL 编排**: Extract → Transform → Load 全流程自动化
- **实时流处理**: Kafka / Kinesis 流式数据处理
- **Schema 管理**: 自动 Schema 演进、兼容性检查
- **数据质量**: 自动数据质量检测，行数/空值/异常值监控
- **回填机制**: 支持历史数据回填与增量同步
- **告警驱动**: 数据异常自动告警 (Slack/Email/PagerDuty)

## 支持数据源
- PostgreSQL, MySQL, MongoDB
- S3, GCS, BigQuery
- Kafka, Kinesis, Redpanda

## 配置文件
- `config/connections.yaml` — 数据源连接配置
- `config/pipelines/` — Pipeline 定义

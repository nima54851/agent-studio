# Backup & Disaster Recovery Automation

> 多层备份策略：数据库快照、文件备份、S3/OSS 跨区域复制、Restic 增量备份、恢复演练自动化

## 概述

自动化备份与灾难恢复系统。支持 MySQL/PostgreSQL/MongoDB 自动快照、S3/OSS 跨区域复制、Restic 增量备份、以及定期恢复演练确保备份可用性。

## 核心能力

- **数据库备份**：MySQL、PostgreSQL、MongoDB 自动快照 + 压缩
- **文件备份**：Restic / Borg 增量备份，支持去重
- **云存储复制**：S3 / OSS / GCS 跨区域/跨账号复制
- **版本管理**：保留 N 个备份版本，自动清理过期备份
- **加密**：AES-256 端到端加密备份数据
- **恢复演练**：定期自动恢复测试，验证备份有效性
- **告警**：备份失败/恢复失败实时通知

## 备份策略矩阵

| 数据类型 | 频率 | 保留 | 目的地 |
|---------|------|------|--------|
| PostgreSQL | 每6小时 | 7天每日 + 4周每周 | S3 + 本地 |
| 文件目录 | 每日 | 30天 | Restic仓库 |
| MongoDB | 每小时 | 24小时每小时 | S3 |
| 配置/密钥 | 变更时 | 90天 | OSS + 异地 |

## 工作流

```json
// integrations/backup-disaster-recovery-automation/backup-pipeline.json
// 节点: Cron (每6h) → PG Dump + File Backup → Compress+Encrypt → S3 Primary + S3 DR → Restic Verify → Alert on Fail
```

## 配置

| 参数 | 说明 |
|------|------|
| `BACKUP_SOURCE_DIR` | 备份源目录 |
| `Restic_PASSWORD` | Restic 加密密码 |
| `S3_BUCKET_PRIMARY` | 主备份桶 |
| `S3_BUCKET_DR` | 异地灾备桶 |
| `RETENTION_DAYS` | 保留天数 |
| `SLACK_CHANNEL` | 告警频道 |

## 恢复命令

```bash
# PostgreSQL 恢复
pg_restore -h localhost -U postgres -d mydb latest_backup.dump

# Restic 恢复
restic -r s3:https://s3.amazonaws.com/bucket restore latest --target /restore
```

## 开始使用

1. 配置存储凭证（S3/OSS）
2. 安装 Restic: `curl -s https://restic.net/install.sh | bash`
3. 导入 `integrations/backup-disaster-recovery-automation/backup-pipeline.json`
4. 配置 Cron 触发时间和恢复演练计划

## 相关技能

- `database-automation`：数据库管理
- `multi-agent-coordination`：多步骤编排

---

*版本 1.0 | 2026-08-01*

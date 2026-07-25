# On-Call Rotation Automation

> 值守轮班自动化 — PagerDuty/OpsGenie 排班、升级策略、交接 AI 摘要、疲劳度管理

## 核心能力

- **智能排班**：支持覆盖地区/时区/技能偏好，自动生成循环排班表
- **升级链路**：P0→P1→P2→Manager 自动升级，含超时触发器
- **AI 交接摘要**：值守结束时自动生成 S.O.S. 摘要（进行中告警/待办/上下文）
- **值班疲劳度**：追踪个人告警处理量，自动均衡分配，避免过度值班
- **事后复盘**：告警关闭后自动触发 post-mortem 生成，关联 change events
- **Runbook 集成**：告警触发时自动推送对应 Runbook 链接

## 工具清单

| 工具 | 说明 |
|---|---|
| PagerDuty API | 排班 + 告警事件 |
| OpsGenie API | 备选集成 |
| Google Calendar API | 排班日历同步 |
| OpenAI / Claude | AI 摘要生成 |
| Slack / Discord | 通知推送 |
| n8n | 全链路自动化 |

## n8n 集成

`integrations/oncall-rotation-automation/oncall-workflow.json`

- PagerDuty Incident Webhook → 提取告警上下文 → AI 生成初步诊断
- 告警超时 → 自动升级 → 发 Slack 给下一级
- 值守交接（定时） → 抓取进行中告警 → AI 摘要生成 → 发送交接报告
- 每周排班生成 → 发布到 Google Calendar → 同步到 Slack 频道

## 排班配置示例

```yaml
# oncall-schedule.yaml
rotation:
  type: weekly
  timezone: Asia/Shanghai
  members:
    - name: Alice
      skills: [backend, database]
      no_go: [weekends]
    - name: Bob
      skills: [frontend, infra]
    - name: Carol
      skills: [security]
      backup: true

escalation:
  - level: 1
    timeout: 15m
    target: oncall_engineer
  - level: 2
    timeout: 30m
    target: team_lead
  - level: 3
    timeout: 1h
    target: vp_engineering
```

## 使用场景

- SRE 团队值班管理
- 告警疲劳度治理
- 跨时区 DevOps 团队
- 重大故障快速升级

## 相关技能

- `incident-response-automation` — 事件响应
- `cross-platform-notification` — 多渠道通知
- `monitoring-alerting-automation` — 监控告警

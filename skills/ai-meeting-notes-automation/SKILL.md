# AI Meeting Notes Automation

## 描述
自动生成会议纪要：从 Zoom/Meet 录音 → Whisper STT → LLM 摘要 → Notion/Confluence 存档，支持 Action Items 提取与责任人分配。

## 触发条件
- 用户上传会议录音
- 同步日历事件触发
- Webhook 接收会议结束通知

## 核心能力
- Whisper STT 多语言转写
- LLM 摘要：要点、决策、待办
- 自动提取 Action Items（人名 + 任务 + deadline）
- 写入 Notion / Confluence / Slack
- 支持时间戳标记（快速跳转到关键段落）

## 使用方式
```bash
# 触发工作流
curl -X POST webhook_url -d '{"recording_url": "...", "meeting_title": "..."}'
```

## n8n 工作流
`integrations/ai-meeting-notes-automation/n8n-meeting-notes-workflow.json`

## 来源
本技能整合 Whisper + GPT-4o + Notion API 构建

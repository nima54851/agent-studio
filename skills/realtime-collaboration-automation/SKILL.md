# Realtime Collaboration Automation

实时协作自动化技能——让 AI Agent 参与团队实时工作流，同步上下文、协调多人任务。

## 🎯 功能

- **多人任务协调**：自动分发任务、追踪 assignee、生成 standup 摘要
- **实时状态同步**：WebSocket/Yjs CRDT 文档协作、冲突检测
- **会议 AI 助理**：实时转录 + 决策点提取 + 会议摘要
- **Code Review 协作**：PR 实时讨论、审查状态自动更新

## 🛠️ 核心工具

| 工具 | 用途 |
|---|---|
| `cable-ready` | WebSocket 实时推送（通知、状态变化） |
| `yjs-crdt` | 多端文档协作（冲突无关） |
| `Liveblocks` | 协作白板、评论、Cursor 实时 |
| `Hocuspocus` | Yjs 服务器（持久化 CRDT） |
| `Vocus AI` | 实时会议 AI 助理 |

## 📁 目录结构

```
realtime-collaboration-automation/
├── SKILL.md                   # 本文件
├── README.md                  # 详细文档
├── n8n-realtime-collaboration.json   # n8n workflow
└── scripts/
    ├── meeting_summarizer.py  # 会议摘要生成
    └── task_coordinator.py    # 任务协调脚本
```

## 🔧 使用方式

```bash
# 启动会议摘要服务
python3 scripts/meeting_summarizer.py --meeting-id <id>

# 协调任务分发
python3 scripts/task_coordinator.py --project <project-id>
```

## 🔗 集成

- **n8n**: `n8n-realtime-collaboration.json` 包含完整协作 pipeline
- **OpenClaw**: 可通过 MCP 调用本技能，实现团队 AI 协调
- **Slack/Discord**: 实时通知发送到协作频道

## 📊 输出示例

```
📋 今日 Standup 摘要:
- 张三: 完成登录页 (PR #42)
- 李四: 修复支付 bug (进行中)
- 王五: API 文档 (待 Review)
🤖 AI 建议: 优先 Review PR #42（阻塞后续联调）
```

---

*版本 1.0 | 2026-07-26*

# 🤖 agent-studio

<div align="center">

**AI Agent 开发者的生产工具箱**

*Skills · Scripts · Workflows · Automation*

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/nima54851/agent-studio/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/nima54851/agent-studio?style=flat)](https://github.com/nima54851/agent-studio/stargazers)
[![Daily Ops](https://img.shields.io/badge/Daily%20Ops-09:00%20Beijing-22d3ee?style=flat&logo=github-actions)](https://github.com/nima54851/agent-studio/actions)

> 开源 MIT · 免费商用 · 持续更新

</div>

---

## 🎯 这是什么

agent-studio 是一个**面向 AI Agent 开发者的开源工具箱**，包含：

| 类别 | 内容 | 数量 |
|------|------|------|
| ⚙️ Skills | OpenClaw Agent Skills（记忆、MCP、监控等） | 4 |
| 🐍 Scripts | Python 工具脚本（Trending、MCP Client 等） | 4 |
| ⚡ Workflows | n8n 工作流模板 + GitHub Actions CI | 2+ |
| 🔧 自动化 | 每日自动运营系统（评论、Star、报告） | ✅ |

---

## 🚀 快速开始

```bash
# Clone
git clone https://github.com/nima54851/agent-studio
cd agent-studio

# 运行热点追踪
pip install requests
python3 scripts/github_trending.py

# 启动每日自动化（每天 09:00 北京时间）
./daily_scheduler.sh
```

---

## 📦 产品包（付费）

如果你需要**完整可用的自动化系统**，推荐购买产品包：

| 产品 | 价格 | 链接 |
|------|------|------|
| 入门版 | 免费 | [GitHub 下载](products/github-agent-automation/) |
| 专业版 | ¥299 | [联系购买](https://github.com/nima54851/agent-studio/issues) |
| 企业版 | ¥999 | [联系购买](https://github.com/nima54851/agent-studio/issues) |

👉 **查看产品详情：https://nima54851.github.io/agent-studio/product.html**

---

## 🧭 项目结构

```
agent-studio/
├── skills/                          # OpenClaw Agent Skills
│   ├── agent-memory/                # 长期记忆系统
│   ├── github-trending-monitor/     # GitHub 热点监控
│   ├── mcp-integration/            # MCP 生态集成
│   └── webhook-dispatcher/         # Webhook 事件分发
├── scripts/                         # Python 工具脚本
│   ├── github_trending.py          # GitHub Trending 爬虫
│   ├── mcp_client.py               # MCP Python 客户端
│   ├── memory.py                   # AgentMemory 类
│   └── webhook_dispatcher.py       # Webhook 分发器
├── workflows/                       # n8n 工作流
│   ├── github-ai-digest.json       # n8n 工作流 JSON
│   └── github-ai-digest-runbook.md # 部署手册
├── products/                        # 付费产品包
│   └── github-agent-automation/    # 社交媒体自动运营系统
├── docs/                           # GitHub Pages 网站
│   ├── index.html                  # 主站
│   └── product.html                # 产品销售页
├── daily_ops.py                    # 每日自动化脚本
├── daily_scheduler.sh              # 每日调度脚本
└── .github/workflows/daily-report.yml  # GitHub Actions
```

---

## ⚡ 核心功能

### 🤖 Agent Skills
开箱即用的 OpenClaw Agent Skills，让 AI Agent 具备特定能力：

- **agent-memory** — 结构化长期记忆系统，Agent 永不忘事
- **github-trending-monitor** — 每天自动追踪 AI/ML 热点
- **mcp-integration** — MCP（Model Context Protocol）生态集成指南
- **webhook-dispatcher** — 通用 Webhook 事件分发系统

### 🔍 Scripts
生产级 Python 脚本，可独立使用或集成到其他系统：

- **github_trending.py** — GitHub Trending API 抓取，支持多语言过滤
- **mcp_client.py** — MCP HTTP/SSE + stdio 客户端，交互式 REPL
- **memory.py** — 基于文件的 AgentMemory 实现
- **webhook_dispatcher.py** — Webhook 事件路由和分发

### ⚡ Workflows
n8n 工作流模板，导入即用：

- **GitHub AI Digest** — 每天自动生成 AI 资讯报告并推送

---

## 💰 变现路径

使用 agent-studio 的开发者可以实现以下变现：

```
免费使用 → 积累影响力 → 接单赚钱 → 模板销售 → SaaS 产品
```

### 路线 1：卖服务
帮别人搭建 AI Agent 系统，接单平台：
- 程序员客栈 / 码市
- Upwork / Fiverr（英文市场，报价 $30-300/hr）
- 闲鱼 / 小红书

### 路线 2：卖模板包
打包工作流模板，在 Gumroad 或微信小店销售：
- 定价 ¥99-299/套
- 成本为零，边际成本为零

### 路线 3：GitHub Sponsors
Star 数达到 100+ 后，申请 GitHub Sponsors 收款

### 路线 4：内容变现
录制教程视频，上传 B站/YouTube，接广告和付费订阅

---

## 🔧 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.10+ | 核心脚本 |
| OpenClaw | AI Agent 框架 |
| n8n | 工作流自动化 |
| GitHub API | 数据源 |
| GitHub Actions | CI/CD |
| GitHub Pages | 在线文档 |

---

## 📄 许可证

MIT License — 可商用、可修改、可分发

---

## 👤 作者

**nima54851**（万）
- GitHub: https://github.com/nima54851
- AI Agent 开发者 · 自动化流水线搭建 · GitHub Trending 每日追踪

*Built with 灵犀 AI · Powered by OpenClaw*

[![Star History](https://api.star-history.com/svg?repos=nima54851/agent-studio&type=Date)](https://star-history.com/#nima54851/agent-studio&Date)

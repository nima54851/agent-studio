# AI Agent 社交媒体自动运营系统

> 全自动 GitHub 账号运营 · 无需写代码 · 5 分钟上线

---

## 🚀 功能一览

| 模块 | 说明 | 状态 |
|---|---|---|
| ⏰ 自动定时 | 每天 09:00 北京时间自动运行 | ✅ |
| 🔍 热点追踪 | 抓取当天 AI/ML 热门项目 | ✅ |
| ✍️ AI 评论 | GPT 生成高质量技术评论 | ✅ |
| ⭐ 自动 Star | 每天自动 Star 优质项目 | ✅ |
| 📊 报告生成 | 自动生成每日资讯报告 | ✅ |
| 📡 多平台推送 | 支持 Telegram / 邮件 / Webhook | ✅ |

---

## 📦 产品包含

```
github-agent-automation/
├── workflow.json    ← n8n 工作流，直接导入
├── README.md        ← 本文件
└── SETUP.md         ← 5分钟部署指南
```

---

## ⚡ 快速部署（5分钟）

### 第一步：准备 Token

1. **GitHub Token**
   - 访问：https://github.com/settings/tokens
   - 生成新 Token（classic），勾选 `repo` scope
   - 复制保存（格式：`ghp_xxxx`）

2. **OpenAI API Key（可选，用于 AI 评论生成）**
   - 访问：https://platform.openai.com/api-keys

### 第二步：导入 n8n

```bash
# 1. 打开 n8n
http://localhost:5678

# 2. 点击右上角「Import from File」
# 3. 上传 workflow.json

# 4. 配置凭证
#    - GitHub API：填入 GitHub Token
#    - Email SMTP（如需要）：填入邮箱配置
```

### 第三步：修改配置

在 n8n 编辑器中修改以下节点：

```
💬 发评论/Issue 节点
  → owner: 你的 GitHub 用户名
  → repository: 你的目标仓库

⭐ 自动 Star 节点
  → repoOwner: 要 Star 的仓库所有者
  → repoName: 仓库名

📡 推送 Webhook 节点
  → url: 你的 webhook 地址
```

### 第四步：激活运行

1. 点击右上角 **「Activate」** 按钮
2. 工作流将在每天 09:00 北京时间自动执行
3. 查看 **Executions** 标签确认运行状态

---

## 🛠 架构说明

```
Schedule Trigger (09:00)
        ↓
GitHub API — 抓取 Trending
        ↓
数据整理（提取项目信息）
    ↓           ↓
自动 Star    AI 评论生成
    ↓           ↓
Webhook → Telegram / 邮件
```

---

## ⚙️ 环境要求

- **Node.js**: 18.x+
- **n8n**: 1.x（推荐最新版）
- **GitHub Token**: 具有 repo 权限
- **网络**: 可访问 api.github.com

---

## ❓ 常见问题

**Q: Token 怎么生成？**
A: GitHub → Settings → Developer settings → Personal access tokens → Generate new token → 勾选 `repo` 和 `workflow`

**Q: 每天能运行几次？**
A: GitHub API 免费版 60次/小时，带 Token 5000次/小时

**Q: 如何自定义评论内容？**
A: 在 n8n 的 Code 节点中修改 `jsCode` 部分的 prompt 模板

**Q: 支持其他平台吗？**
A: 支持任意有 Webhook 的平台（Telegram、飞书、钉钉、Discord）

---

## 🔒 安全说明

- Token 建议存储在 n8n 的「Credentials」中，不要硬编码在工作流里
- 生产环境建议使用只读权限的 Token
- 定期轮换 Token（建议每90天）

---

## 📞 技术支持

有问题？请提交 Issue：https://github.com/nima54851/agent-studio/issues

---

## 📄 许可证

MIT License — 可商用，可修改，可分发

**Powered by [agent-studio](https://github.com/nima54851/agent-studio) · Built by [nima54851](https://github.com/nima54851)**

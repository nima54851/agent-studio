# n8n 工作流模板 - 快速上手

## 🚀 快速导入

### 方式一：直接从 GitHub 导入
1. 打开 n8n → 新建工作流
2. 点右上角 `···` → `Import from JSON`
3. 复制 `github-trending-workflow.json` 内容粘贴

### 方式二：手动创建
按 README 中的节点顺序，在 n8n 可视化编辑器中依次添加即可。

---

## 📋 配置步骤

### 1. 获取 Telegram Bot Token
1. Telegram 找 **@BotFather**，发送 `/newbot`
2. 按提示设置机器人名称和用户名
3. 复制获得的 Token（格式：`123456789:ABC-DEF...`）

### 2. 获取 Chat ID
1. Telegram 找 **@userinfobot**，发送任意消息
2. 它会回复你的 Chat ID（纯数字）

### 3. 配置工作流
1. 打开工作流 → 点击 **Telegram 推送** 节点
2. `Chat ID` 填入你的 Chat ID
3. 左侧菜单 → **Credentials** → **Telegram Bot** → 填入 Bot Token

### 4. 激活工作流
- 右上角 **Active** 开关 → 打开
- 每天早上 9 点自动推送

---

## ⏰ 触发时间修改

在 `每日早9点触发` 节点修改 cron 表达式：

| 时间 | Expression |
|------|-----------|
| 每天早上9点 | `0 9 * * *` |
| 每天早上7点 | `0 7 * * *` |
| 每3小时一次 | `0 */3 * * *` |
| 每天晚8点 | `0 20 * * *` |

---

## 🔧 推送渠道替换

如果不用 Telegram，可以换成：

**邮件：** 用 `Email Send` 节点替换 `Telegram 推送`
- 需要配置邮件 SMTP 凭证

**微信：** 用 `ServerChan` 或 `PushPlus` API
- 免费，无需额外配置

**Slack：** 用 `Slack` 节点
- 需要 Incoming Webhook URL

---

## ❓ 常见问题

**Q: 收不到推送？**
- 检查工作流是否已激活（右上角开关打开）
- 检查 Chat ID 是否正确（必须是数字格式）
- 检查 Bot Token 是否有效

**Q: 如何推送给多个群/用户？**
- 在 Telegram 节点后添加 `Split In Batches` 节点
- 循环发送多个 Chat ID

**Q: 可以在自己的 n8n 实例运行吗？**
- 可以，所有节点都是 n8n 内置节点
- 无需额外安装任何包

---

## 📞 获取帮助

遇到问题 → [GitHub Issues](https://github.com/nima54851/agent-studio/issues)

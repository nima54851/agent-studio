# Automated Release Notes

> 从 Git Commits、PRs、Issues 自动生成结构化 Release Notes，支持 Conventional Commits、Semantic Versioning

## 概述

告别手动写 Release Notes的痛苦。每次合并主分支时，自动分析 commits、PRs、issues，生成符合 CHANGELOG.md 格式的发布说明。

## 核心能力

- **Commit 解析**：Conventional Commits 自动分类（feat/fix/docs/style/refactor/test/perf）
- **PR 合并信息**：从 GitHub API 提取 PR 标题、描述、作者、标签
- **Issue 摘要**：关联的 closed issues 自动归类到对应功能
- **Semantic Versioning**：根据变更类型自动计算版本号（major/minor/patch）
- **多格式输出**：Markdown、GitHub Releases、Slack、Email
- **AI 增强**：LLM 生成人类可读的自然语言描述

## 工作流

```
Merge to main → GitHub Webhook → Fetch commits/PRs/issues → LLM 生成 → Create Release + Update CHANGELOG → Notify
```

## 集成

```json
// integrations/automated-release-notes/release-notes-pipeline.json
// 节点: GitHub Webhook → GitHub API (get commits) → AI Classify → LLM Generate → GitHub Create Release
```

## 配置

| 环境变量 | 说明 |
|---------|------|
| `GITHUB_TOKEN` | GitHub PAT |
| `OPENAI_API_KEY` | LLM 生成描述 |
| `SLACK_WEBHOOK` | 发布通知 |

## 开始使用

1. 导入 `integrations/automated-release-notes/release-notes-pipeline.json` 到 n8n
2. 设置 GitHub Webhook 触发条件
3. 配置环境变量
4. 在 GitHub 设置 Webhook → Push events → 指向 n8n webhook URL

## 相关技能

- `github-actions-automation`：GitHub CI/CD
- `ai-document-intelligence`：AI 文档处理

---

*版本 1.0 | 2026-08-01*

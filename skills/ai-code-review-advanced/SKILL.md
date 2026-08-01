# AI Code Review Advanced

> AI 驱动的代码审查进阶版：安全漏洞扫描、性能分析、架构问题检测、带修复建议的对话式审查

## 概述

比基础代码审查更深入的安全 + 性能 + 架构三重 AI 审查。集成 Semgrep、Gitleaks、Complexity Analyzer，自动生成带修复代码的审查报告。

## 核心能力

- **安全扫描**：OWASP Top 10、SQL注入、XSS、SSRF、Secret 泄露（Gitleaks）
- **性能分析**：循环复杂度、算法复杂度、N+1 查询检测
- **架构审查**：依赖关系、循环依赖、过重类、违反 SOLID 原则
- **对话式修复**：AI 逐行解释问题并给出修复代码
- **PR 自动评论**：审查结果自动发布到 GitHub PR
- **风险评分**：0-100 综合风险评分
- **多语言支持**：Python / JavaScript / TypeScript / Go / Rust

## 工作流

```json
// n8n workflow: GitHub PR webhook → AI Code Review → Semgrep Scan → Security/Perf/Architecture Analysis → PR Comment + Risk Score
```

## 配置

| 环境变量 | 说明 |
|---------|------|
| `GITHUB_TOKEN` | GitHub PAT |
| `OPENAI_API_KEY` | GPT-4 API Key |
| `SEMGREP_RULES` | 自定义 Semgrep 规则集 |

## 相关技能

- `code-review-automation`：基础 AI 代码审查
- `security-auditor`：安全扫描

---

*版本 1.0 | 2026-08-01*

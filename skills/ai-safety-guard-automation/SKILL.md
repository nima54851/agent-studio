# AI Safety Guard Automation

> 给 AI Agent 加一层安全护栏：输入过滤、输出审查、越狱检测、敏感信息脱敏、危险工具拦截

## 概述

AI Safety Guard Automation 是一套面向 Agent 的纵深防御（Defense in Depth）方案。它在 LLM 调用的前后各插一道关卡，把越狱攻击、提示注入、敏感数据外泄、危险工具调用挡在生产环境之外。

## 核心功能

- **输入护栏（Input Guard）**: 提示注入 / 越狱模式检测、提示词泄露探测
- **输出护栏（Output Guard）**: 有害内容、PII、密钥、代码注入扫描
- **敏感信息脱敏（PII Redaction）**: 邮箱、手机号、身份证、银行卡、API Key 自动遮蔽
- **工具权限管控**: 白名单 / 黑名单工具调用拦截，高危操作二次确认
- **审计日志**: 所有拦截事件留痕，支持回溯与合规导出
- **多引擎评分**: 规则引擎 + 分类模型（零样本）双通道打分，取最高风险分

## 风险评分模型

```
risk = max(rule_score, model_score)
risk >= 0.85  → BLOCK    硬拦截
risk >= 0.60  → REVIEW   转人工 / 降级回复
risk >= 0.30  → WARN     标注但放行
risk <  0.30  → PASS     正常放行
```

## 使用方式

```python
from safety_guard import Guard

guard = Guard(
    pii_redaction=True,
    block_tools=["shell_exec", "file_delete"],
    audit_log="./audit/safety.jsonl",
)

result = guard.check_input(user_text)
if result.action == "BLOCK":
    return {"blocked": True, "reason": result.reasons}

out = llm.chat(result.sanitized)
result = guard.check_output(out)
return result.sanitized
```

## 配置

```json
{
  "thresholds": { "block": 0.85, "review": 0.6, "warn": 0.3 },
  "pii": {
    "email": "mask",
    "phone": "mask",
    "id_card": "mask",
    "bank_card": "mask",
    "api_key": "redact"
  },
  "tool_policy": {
    "allow": ["search", "read_file", "http_request"],
    "deny": ["shell_exec", "sudo", "credential_dump"]
  },
  "audit": { "enabled": true, "path": "./audit/safety.jsonl", "retention_days": 90 }
}
```

## 常见拦截规则

| 类别 | 示例特征 | 处置 |
|---|---|---|
| 提示注入 | "ignore previous instructions"、伪造 system 标记 | BLOCK |
| 越狱 | DAN / 开发者模式 / "pretend you are" | BLOCK |
| 凭据泄露 | sk-、ghp_、AWS AKIA、私钥块 | REDACT |
| 工具滥用 | 删除文件、提权、外发内网数据 | BLOCK |
| 有害内容 | 暴力、自伤、恶意软件 | REVIEW |

## n8n 工作流

参见 `integrations/ai-safety-guard-automation/n8n-safety-guard.json`：

```
Agent 调用 → 输入护栏 → LLM → 输出护栏 → 工具策略 → 结果/拦截/人工复核
```

## 目录结构

```
skills/ai-safety-guard-automation/
├── SKILL.md
└── README.md
integrations/ai-safety-guard-automation/
├── SKILL.md
├── README.md
└── n8n-safety-guard.json
```

## 最佳实践

1. **默认脱敏**：PII 遮蔽默认开启，脱敏比拦截更少打扰用户
2. **分层阻断**：规则引擎负责确定性拦截，模型负责语义判断
3. **可解释**：每条拦截都带 `reason` 与命中规则，便于调试
4. **审计不可关**：审计日志建议写独立存储（只追加），便于合规
5. **灰度上线**：新规则先以 WARN 模式运行一周，再升级为 BLOCK

## 相关技能

- `agent-guardian` — Agent 运行期守护
- `security-auditor` — 安全审计
- `ai-content-moderation` — 内容审核
- `privacy-compliance-automation` — 隐私合规

# AI Safety Guard Automation

AI Agent 安全护栏技能包 —— 输入过滤 / 输出审查 / PII 脱敏 / 工具管控。

## 快速安装

```bash
cp -r skills/ai-safety-guard-automation ~/.openclaw/workspace/skills/
cp -r integrations/ai-safety-guard-automation ~/.openclaw/workspace/skills/
```

## 能力清单

| 能力 | 说明 |
|---|---|
| Input Guard | 提示注入 / 越狱检测 |
| Output Guard | 有害内容 / 密钥泄露扫描 |
| PII Redaction | 邮箱、手机号、身份证、银行卡、API Key 遮蔽 |
| Tool Policy | 工具白名单黑名单、高危操作拦截 |
| Audit Log | 拦截事件审计留痕 |
| Risk Scoring | 规则 + 模型双通道风险评分 |

## 与 n8n 集成

导入 `n8n-safety-guard.json` 即可获得一条完整的护栏管道：
Webhook 触发 → 输入检查 → LLM → 输出检查 → 工具校验 → 放行或拦截。

## 版本

- v1.0.0

# AI Sandbox Isolation Automation

Agent 运行时沙箱技能包 —— 文件/命令/网络三层隔离 + 配额熔断 + 用完即焚。

## 快速安装

```bash
cp -r skills/ai-sandbox-isolation-automation ~/.openclaw/workspace/skills/
cp -r integrations/ai-sandbox-isolation-automation ~/.openclaw/workspace/skills/
```

## 能力清单

| 能力 | 说明 |
|---|---|
| Filesystem Sandbox | 临时工作区、根目录只读、产物统一回收 |
| Command Allowlist | 命令白名单 + 参数黑名单 + 危险模式拦截 |
| Network Egress Policy | 域名白名单、代理转发、一键断网 |
| Quota Breaker | 时长/内存/输出/实例数四维配额熔断 |
| Ephemeral Cleanup | 用完即焚，仅保留审计元数据 |
| Audit Trail | 每次执行写 JSONL 审计记录 |

## 典型场景

- 让 Agent 能跑代码，但碰不到宿主机文件
- 让 Agent 能上网，但只能访问白名单 API
- 让 Agent 不能删文件，但可以读文件
- 单次任务失控时自动掐断，不拖垮整机

## 与 n8n 集成

导入 `n8n-sandbox-isolation.json` 即可获得一条完整沙箱管道：
Webhook 触发 → 策略装配 → 沙箱执行 → 配额校验 → 产物回收 → 审计留痕 → 返回结果。

## 版本

- v1.0.0

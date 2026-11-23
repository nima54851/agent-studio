# AI Sandbox Isolation Automation

> 给 Agent 套一层运行时沙箱：文件/命令/网络三重隔离 + 配额熔断 + 用完即焚

## 概述

Agent 拿到 shell 和网络权限之后，"能做什么"和"敢做什么"之间隔着一道鸿沟。Sandbox Isolation 把 Agent 的每次执行关进一个受限上下文里：写操作只能在临时目录，命令走白名单，出网走代理并可断网，资源超配额立刻中止。

本技能面向 n8n + OpenClaw 场景，提供可落地的三层隔离方案与熔断策略。

## 三层隔离模型

```
┌─────────────────────────────────────────────┐
│ Layer 1  文件隔离 (Filesystem Sandbox)       │  chroot/tmpfs + 只读根 + 临时工作区
├─────────────────────────────────────────────┤
│ Layer 2  命令隔离 (Command Allowlist)       │  允许列表 + 参数黑名单 + 危险模式拦截
├─────────────────────────────────────────────┤
│ Layer 3  网络隔离 (Network Egress Policy)    │  域名白名单 + 代理 + 强制断网开关
└─────────────────────────────────────────────┘
                    ↓
            配额熔断 (Quota Circuit Breaker)
```

## 核心能力

- **文件隔离**：工作目录自动切换到临时沙箱，根目录只读，写入产物统一收集到 exit 目录
- **命令治理**：命令白名单（git/ls/cat/python/node…）+ 参数级黑名单（`rm -rf /`、`curl | sh`、反引号注入）
- **网络出口控制**：域名白名单（api.openai.com 等），非白名单域名直接 DROP，可一键 kill switch 断网
- **资源配额**：CPU 时间、内存、输出字节数、调用次数四维配额，任一超限即中止
- **用完即焚**：任务结束后销毁沙箱目录，仅保留审计元数据（哈希 + 耗时 + 退出码）
- **审计留痕**：每次沙箱执行产生 JSONL 记录，可回溯

## 风险阈值

| 维度 | 软限 | 硬限 | 超限动作 |
|---|---|---|---|
| 单次执行时长 | 60s | 300s | 软限告警，硬限 SIGKILL |
| 内存峰值 | 512MB | 1GB | 软限告警，硬限 OOM |
| 输出字节 | 10MB | 50MB | 软限截断，硬限中止 |
| 沙箱实例数 | 20 | 50 | 拒绝新实例 |

## 使用方式

```python
from sandbox import Sandbox, SandboxPolicy

policy = SandboxPolicy(
    allowed_commands=["ls", "cat", "git", "python3"],
    blocked_patterns=[r"rm\s+-rf", r"curl.*\|\s*sh", r"chmod\s+777"],
    network_allowlist=["api.openai.com", "api.github.com"],
    network_enabled=True,
    max_seconds=120,
    max_output_bytes=10 * 1024 * 1024,
)

with Sandbox(policy, workdir="./workspace") as sb:
    result = sb.run("git status")
    if result.timed_out:
        sb.kill()
    artifacts = sb.collect()
```

## 最佳实践

1. 默认网络关闭，确有需要再开白名单，而不是反过来
2. 沙箱工作目录与宿主工作目录物理隔离，不做软链接穿透
3. 高危命令（rm/mkfs/chown）一律走人工确认分支
4. 沙箱审计日志与业务日志分离存放，便于事后合规审查

## 相关技能

- [ai-safety-guard-automation](../ai-safety-guard-automation/) — 输入输出侧的护栏，与本技能互补
- [security-auditor](../security-auditor/) — 代码与依赖安全审计
- [budget-management-automation](../budget-management-automation/) — 成本侧预算告警

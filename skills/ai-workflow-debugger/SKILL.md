# AI Workflow Debugger

> AI 驱动的自动化流程调试 — 执行轨迹分析、断点推荐、异常根因定位

## 核心能力

- **执行轨迹解析**：解析 n8n/Prefect/Airflow 执行日志，提取每步输入输出
- **异常根因定位**：AI 分析失败节点的上下游依赖，定位根因节点
- **断点推荐**：根据执行频率/错误率/耗时，智能推荐断点位置
- **修复建议**：生成针对性的修复代码/Prompt，对应到具体节点
- **回归测试**：自动生成边界 case，确保修复不引入新问题

## 工具清单

| 工具 | 说明 |
|---|---|
| n8n Execution API | 执行记录读取 |
| LangSmith / Helicone | LLM 调用追踪 |
| Prometheus + Loki | 指标与日志 |
| AI (GPT-4o / Claude) | 分析引擎 |
| n8n | 自动化调试 pipeline |

## n8n 集成

`integrations/ai-workflow-debugger/n8n-workflow-debugger.json`

- 触发：n8n execution webhook / 失败通知
- 提取：执行链、节点耗时、错误堆栈
- 分析：AI 诊断 → 生成报告
- 修复：自动 patch 节点配置 / 发送通知

## 使用场景

- n8n workflow 调试效率提升
- 多步骤 AI pipeline 问题定位
- 定时任务失败根因分析
- CI 中自动化流程回归检测

## 核心 Prompt

```
你是一个工作流调试专家。给定一个 n8n workflow 的执行记录（JSON），
请：1) 找出失败的节点；2) 分析上下游依赖；
3) 给出根因假设；4) 提供具体修复步骤。
```

## 相关技能

- `error-tracking-automation` — 错误追踪
- `workflow-orchestration` — 工作流编排
- `testing-automation` — 自动化测试

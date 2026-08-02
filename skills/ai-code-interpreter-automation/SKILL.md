# AI Code Interpreter Automation

> 沙箱代码执行引擎：让 AI Agent 安全运行 Python / JavaScript / Shell 代码

## 概述

本技能提供一套完整的代码解释器（Code Interpreter）实现方案，支持在隔离沙箱中安全执行 AI 生成的代码，并返回结构化结果（输出、图表、文件）。

适用场景：数据分析、AI Agent 代码执行、自动化报告生成、交互式 Notebook。

## 核心能力

- **多语言支持**：Python、JavaScript、Shell、Bash
- **沙箱隔离**：Docker 容器 / eBPF 微隔离 / 资源限制（CPU/内存/时间）
- **持久化会话**：保持状态，支持变量跨代码块传递
- **文件生成**：支持生成 CSV、图表（matplotlib/plotly）、PDF、图片
- **n8n 集成**：Webhook 触发 → 代码执行 → 结果推送

## 文件结构

```
ai-code-interpreter-automation/
├── SKILL.md                    ← 本文件
├── README.md                   ← 详细文档
├── configs/
│   └── sandbox_config.json     ← 沙箱资源配置
├── runner/
│   ├── interpreter.py           ← 主解释器
│   ├── sandbox.py              ← 沙箱隔离层
│   └── executor.py             ← 多语言执行器
├── prompts/
│   └── code_executor_prompt.md ← AI 执行 Prompt
├── n8n_workflow.json           ← n8n 工作流
└── examples/
    ├── data_analysis.py        ← 数据分析示例
    └── chart_generation.py     ← 图表生成示例
```

## 快速使用

### Python 执行示例

```python
from runner.interpreter import CodeInterpreter

interpreter = CodeInterpreter(
    sandbox_mode="docker",     # docker / subprocess / eBPF
    timeout=30,
    max_memory_mb=512,
    max_output_lines=500
)

# 单次执行
result = interpreter.execute("""
import pandas as pd
df = pd.DataFrame({'sales': [100, 200, 300], 'region': ['A', 'B', 'C']})
print(df.describe())
print("Total:", df['sales'].sum())
""")

print(result.stdout)    # 控制台输出
print(result.stderr)    # 错误信息
print(result.files)     # 生成的文件列表
print(result.elapsed_ms) # 执行耗时
```

### 持久化会话

```python
session = interpreter.create_session()

session.execute("data = [1, 2, 3, 4, 5]")
session.execute("import statistics")
result = session.execute("statistics.mean(data)")
print(result.stdout)  # 3.0（可访问前面定义的 data）
```

### 文件生成 + 图表

```python
result = interpreter.execute("""
import matplotlib.pyplot as plt

months = ['Jan', 'Feb', 'Mar', 'Apr']
sales = [120, 200, 150, 300]

plt.figure(figsize=(10, 6))
plt.plot(months, sales, marker='o', linewidth=2)
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales ($)')
plt.grid(True)
plt.savefig('/tmp/sales_chart.png', dpi=150)
print("Chart saved: /tmp/sales_chart.png")
""")

print(result.files)  # ['/tmp/sales_chart.png']
```

## 沙箱配置

```json
{
  "sandbox": {
    "mode": "docker",
    "image": "python:3.11-slim",
    "network": "none",
    "readonly_fs": false,
    "resources": {
      "max_cpu_percent": 50,
      "max_memory_mb": 512,
      "max_execution_seconds": 30,
      "max_output_lines": 1000
    },
    "allowed_packages": ["pandas", "numpy", "matplotlib", "plotly", "scikit-learn"],
    "blocked_imports": ["os", "sys", "subprocess", "socket"]
  },
  "security": {
    "enable_strict_mode": true,
    "scan_for_secrets": true,
    "rate_limit_per_minute": 10
  }
}
```

## n8n 工作流

```
用户请求（Webhook）
    ↓
代码接收 → 安全扫描（检测危险 API）
    ↓
沙箱执行（Docker 隔离）
    ↓
结果收集（stdout + 文件 + 错误）
    ↓
格式化输出 → Slack/Email 推送
```

## 安全防护

| 防护层 | 措施 |
|--------|------|
| 导入拦截 | 禁止 `os`、`subprocess`、`socket` 等系统调用 |
| 资源限制 | CPU 50%、内存 512MB、超时 30s |
| 网络隔离 | Docker 网络 `none` 模式 |
| 敏感检测 | 扫描代码中的 API Key、密码检测 |
| 速率限制 | 每分钟最多 10 次执行 |

## 与其他技能的关系

- `testing-automation`：代码执行后自动跑测试
- `data-visualization-automation`：复用图表生成能力
- `agent-skills-kit`：作为 Agent 的工具之一

---

*版本 1.0 | 适用于 agent-studio*

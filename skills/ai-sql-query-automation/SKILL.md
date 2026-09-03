# AI SQL Query Automation

## 描述
自然语言转 SQL 查询，支持 PostgreSQL / MySQL / SQLite / MongoDB，自动生成 JOIN、聚合、窗口函数，附查询解释与性能建议。

## 触发条件
- 用户要求查询数据库
- 提供 schema 或表结构描述
- 需要生成 SELECT / INSERT / UPDATE / DELETE / ALTER 语句

## 核心能力
- 自然语言 → SQL（支持 5 种方言）
- SQL 解释：告诉用户每句在做什么
- 性能评估：指出 N+1、全表扫描风险
- 自动加索引建议
- 支持复杂查询：CTE、窗口函数、子查询

## 使用方式
```bash
# 1. 提供表结构
# 2. 描述需求："找出过去30天订单金额超过1000的用户"
# 3. 生成 SQL 并解释
```

## n8n 工作流
`integrations/ai-sql-query-automation/n8n-sql-query-workflow.json`

## 来源
本技能参考 AI sqli / SQLGlot / Vanna.ai 思路构建

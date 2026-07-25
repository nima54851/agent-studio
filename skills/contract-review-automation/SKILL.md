# Contract Review Automation

> AI 合同审查 — 条款提取、风险评分、红线对比、批量审查

## 核心能力

- **条款智能提取**：付款条件/保密协议/违约责任/终止条款自动识别并结构化
- **风险评分**：0-100 分合同风险评级，标注高风险条款（如无限追索权）
- **红线对比**：合同 V1 vs V2 自动 diff，变更条款高亮
- **法律数据库对齐**：对照 NDA/服务协议/SaaS 标准模板，发现缺失条款
- **批量审查**：支持 PDF/DOCX/图片扫描，多合同并行 AI 审查
- **审查报告**：结构化报告 + 执行摘要，支持法务/财务审批流

## 工具清单

| 工具 | 说明 |
|---|---|
| Claude / GPT-4o | 合同理解与条款提取 |
| pdfplumber / PyMuPDF | PDF 解析 |
| python-docx | Word 文档读取 |
| Tesseract OCR | 扫描件识别 |
| n8n | 审查流程编排 |
| Google Docs API | 报告写入 |

## n8n 集成

`integrations/contract-review-automation/contract-review-workflow.json`

- Email/Webhook 接收合同附件
- 文件类型判断 → PDF 解析 / DOCX 读取 / OCR 处理
- AI 条款提取 → 风险评分 → 生成报告
- 高风险条款 → Slack/Email 通知法务
- 报告归档 → Google Drive + CRM 更新

## 审查 Prompt 示例

```python
SYSTEM_PROMPT = """
你是资深商业律师。分析以下合同，输出 JSON：
{
  "summary": "一句话摘要",
  "risk_score": 0-100整数,
  "high_risk_clauses": ["条款描述"],
  "missing_clauses": ["缺失条款"],
  "payment_terms": "付款条件描述",
  "termination": "终止条款描述",
  "confidentiality": "保密期限",
  "liability_cap": "责任上限"
}
"""
```

## 使用场景

- SaaS 服务协议审查
- 供应商合同批量审查
- NDA/MSA 标准模板检查
- M&A 法律尽职调查

## 风险评分标准

| 分数 | 等级 | 说明 |
|---|---|---|
| 0-30 | 🟢 低风险 | 标准条款，可快速通过 |
| 31-60 | 🟡 中风险 | 需法务复核 1-2 处 |
| 61-85 | 🟠 高风险 | 需深度谈判 |
| 86-100 | 🔴 极高风险 | 建议拒绝或重大修改 |

## 相关技能

- `ai-document-intelligence` — 文档解析
- `compliance-automation` — 合规审计
- `sentiment-analysis-automation` — 条款情感分析

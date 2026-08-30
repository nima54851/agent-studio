# 📄 CV/Resume Automation

AI 招聘自动化技能包：简历解析 → 人才评分 → 智能筛选 → 面试安排 → Offer 生成，全流程无人值守。

## 📦 包含内容

- **SKILL.md** — 技能定义与使用说明
- **n8n-cv-parser.json** — 简历解析工作流（PDF/DOCX → 结构化数据）
- **n8n-candidate-scorer.json** — 人才评分工作流（多维度 AI 评分）
- **n8n-interview-scheduler.json** — 面试官分配 + 日历预约工作流
- **n8n-offer-generator.json** — Offer 模板生成工作流
- **scripts/cv_parser.py** — 简历解析主脚本（支持 PDF/DOCX/图片 OCR）
- **scripts/candidate_scorer.py** — 人才多维度评分
- **scripts/interview_scheduler.py** — 智能面试安排
- **scripts/offer_generator.py** — Offer Letter 生成

## 🚀 快速开始

### 简历解析
```bash
pip install pdfplumber python-docx openai
python3 scripts/cv_parser.py resume.pdf --format=json
```

### 人才评分
```bash
python3 scripts/candidate_scorer.py \
  --resume=parsed_resume.json \
  --jd="Job Description content here" \
  --output=score_report.json
```

### n8n 工作流导入
1. n8n → Import → 选择 JSON 文件
2. 配置 OpenAI API Key 和邮件服务凭证
3. Activate

## 功能详情

### 简历解析
- 支持格式：PDF、DOCX、图片（OCR）
- 提取字段：姓名、邮箱、电话、技能、工作经历、教育背景、项目经验
- 格式标准化输出 JSON

### 人才评分维度
| 维度 | 权重 | 说明 |
|------|------|------|
| 技术匹配 | 40% | JD 关键词匹配度 |
| 经验年限 | 20% | 与职位要求的符合度 |
| 教育背景 | 15% | 学历与专业相关性 |
| 文化匹配 | 15% | 远程/加班/价值观 |
| 推荐指数 | 10% | 综合决策建议 |

### 评分输出示例
```json
{
  "candidate": "John Doe",
  "overall_score": 87,
  "recommendation": "Strong Hire",
  "breakdown": {
    "tech_match": 92,
    "experience_years": 85,
    "education": 90,
    "culture_fit": 78,
    "overall": 87
  },
  "matched_skills": ["Python", "React", "PostgreSQL", "Docker"],
  "missing_skills": ["Kubernetes", "GraphQL"],
  "interview_focus": ["System Design", "Leadership Experience"]
}
```

## 适用场景
- HR 团队大规模招聘初筛
- 猎头/招聘平台人才库建设
- 企业内部职位晋升评估

## 集成推荐
- **ATS 系统**：Lever、Greenhouse、Ashby（API 集成）
- **日历**：Google Calendar、Calendly（面试安排）
- **邮件**：SendGrid、Gmail API（Offer 发送）

---
*AI 招聘，从每天读100份简历中解放*

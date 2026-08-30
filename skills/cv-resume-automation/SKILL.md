# 📄 CV/Resume Automation Skill

AI 自动化处理招聘全链路：简历解析、人才评分、智能筛选、面试安排、Offer 发送。

## 能力矩阵

| 能力 | 描述 | 场景 |
|------|------|------|
| 简历智能解析 | PDF/DOCX/图片 → 结构化数据提取 | 人才入库 |
| AI 人才评分 | 多维度（技术/经验/文化匹配）打分 | 初筛 |
| 关键词匹配 | Job Description ↔ Resume 匹配度 | ATS 初筛 |
| 面试官分配 | 根据技能需求 + 日历可用性智能分配 | 调度 |
| Offer 生成 | 基于职级 + 市场薪资自动生成 Offer | 录用 |

## 快速开始

```bash
pip install pdfplumber python-docx openai
python3 scripts/cv_parser.py resume.pdf --format=json
python3 scripts/candidate_scorer.py --resume=parsed.json --jd=job_desc.md
```

## 目录结构
```
cv-resume-automation/
├── SKILL.md
├── README.md
└── scripts/
    ├── cv_parser.py        # 简历解析
    ├── candidate_scorer.py # 人才评分
    ├── interview_scheduler.py # 面试安排
    └── offer_generator.py  # Offer 生成
```

## 简历解析示例

```python
from cv_parser import parse_resume

resume_data = parse_resume("candidate_john.pdf")
# {
#   "name": "John Doe",
#   "email": "john@example.com",
#   "skills": ["Python", "React", "PostgreSQL"],
#   "experience_years": 5,
#   "education": "BS Computer Science, MIT",
#   "summary": "Full-stack engineer with 5 years..."
# }
```

## 人才评分

```python
score = score_candidate(resume_data, job_description)
# 返回: { "overall": 87, "tech_match": 92, "culture_fit": 81, "recommendation": "Strong Hire" }
```

---
*AI 驱动招聘，告别人工筛选简历的繁琐*

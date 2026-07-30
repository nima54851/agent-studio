# AI Interview Automation

> AI-powered technical interview system — resume screening, coding challenge generation, live code evaluation, and candidate scoring. Streamline your hiring pipeline from first touch to final verdict.

## What It Does

- **Resume Screening**: Parse resumes (PDF/DOCX), score against job requirements, rank candidates
- **Coding Challenges**: Generate personalized coding problems based on role (Frontend/Backend/ML/DevOps)
- **Live Code Evaluation**: Sandboxed code execution, test cases, timeout handling, memory limits
- **Technical Questions**: Auto-generate follow-up questions based on candidate's code answers
- **Candidate Scoring**: Multi-dimensional scoring rubric (correctness, efficiency, code quality, communication)
- **Calendar Integration**: Auto-schedule interviews, send reminders via email/Slack

## Skill Capabilities

- Support HackerRank, LeetCode, CodeSignal-style challenges
- LLM-generated personalized questions per candidate
- Real-time WebSocket code editor integration
- Interview notes auto-transcribed with Whisper
- Rejection/offer email templates with personalization
- Diversity-aware scoring (bias reduction)

## Files

- `SKILL.md` — This file
- `resume_parser.py` — Parse and score resumes against job requirements
- `challenge_generator.py` — Generate role-appropriate coding challenges
- `code_evaluator.py` — Sandboxed code execution and test evaluation
- `candidate_scorer.py` — Multi-dimension candidate scoring rubric

## Setup

```bash
pip install pdfplumber python-docx openai
```

## Usage

```python
from resume_parser import ResumeParser
from challenge_generator import ChallengeGenerator

parser = ResumeParser()
resume = parser.parse("candidate_resume.pdf")
score = parser.score_against_requirements(resume, job_requirements)
print(f"Match score: {score}%")

generator = ChallengeGenerator(role="backend")
challenge = generator.generate(role="backend", difficulty="medium", topic="API design")
print(challenge.description)
```

## n8n Integration

Import `n8n-interview-automation.json` to connect:
- Job application webhook → resume screening → coding challenge email → evaluation → score → Slack/email result

## OpenClaw Integration

```python
# skill.py
async def screen_resume(context):
    resume = parser.parse(context.resume_url)
    score = parser.score_against_requirements(resume, context.job_requirements)
    return {"score": score, "top_skills": resume.skills, "gaps": resume.missing}
```

---

*Part of [agent-studio](https://github.com/nima54851/agent-studio) · Built by 灵犀 AI*

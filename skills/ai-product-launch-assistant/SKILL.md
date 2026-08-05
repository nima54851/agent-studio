# AI Product Launch Assistant

> Automate your Product Hunt launch — hunter submission, social buzz, maker updates, and post-launch analytics.

## 🎯 What it does

End-to-end Product Hunt launch automation powered by AI:

1. **Launch Checklist Generator** — AI generates a personalized pre-launch checklist based on your product category
2. **Hunter Outreach** — Finds relevant hunters, crafts personalized pitches, sends outreach emails via n8n
3. **Social Countdown Sequence** — Scheduled Twitter/LinkedIn posts building anticipation
4. **Launch Day Automation** — Posts to PH at optimal time, engages with first commenters
5. **Post-Launch Report** — AI summarizes results: votes, comments, traffic sources, top referrers

## 🛠️ Tools Used

- **GitHub API** — Auto-update README with launch badge
- **n8n** — Workflow orchestration: email sequences, social posts, PH API
- **Hunter.io API** — Find hunter email addresses
- **OpenAI / Claude** — Write personalized hunter pitches and launch copy

## 📁 Structure

```
ai-product-launch-assistant/
├── SKILL.md
├── prompts/
│   ├── launch-checklist.md
│   ├── hunter-pitch.md
│   └── post-launch-report.md
├── scripts/
│   ├── ph_submitter.py
│   ├── hunter_outreach.py
│   └── launch_tracker.py
└── integrations/
    └── n8n/
        └── ph-launch-workflow.json
```

## 🚀 Quick Start

1. Add your PH API credentials to n8n
2. Configure hunter outreach targets in `scripts/hunter_outreach.py`
3. Set launch date and run the n8n workflow
4. Monitor via dashboard

## 📌 Requirements

- n8n instance
- OpenAI API key (AI copywriting)
- Hunter.io API key
- Twitter/X developer account (optional)

---

*Part of [Agent Studio](https://github.com/nima54851/agent-studio)*

# Product Hunt Launch Automation

Automate your Product Hunt launch with AI-powered hunter outreach, social buzz, and post-launch analytics.

## Quick Start

1. Import `n8n/ph-launch-workflow.json` into your n8n instance
2. Set environment variables:
   - `PH_API_KEY` — Product Hunt API key
   - `OPENAI_API_KEY` — AI-generated launch copy
   - `HUNTER_API_KEY` — Hunter email finder
3. Activate the workflow

## Workflow Steps

1. **Cron Trigger** — Daily check for launch window
2. **PH API** — Fetch upcoming launches / submit your product
3. **AI Copy Generator** — Generates tagline, first comment, Twitter posts
4. **Twitter/X Post** — Scheduled social countdown posts
5. **Hunter Outreach** — Personalized email pitches to relevant hunters

## Requirements

- n8n
- OpenAI API key
- Hunter.io API key
- Twitter Developer Account (optional)

*Part of [Agent Studio](https://github.com/nima54851/agent-studio)*

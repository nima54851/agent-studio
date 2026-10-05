# AI Meeting Notes Automation

> Auto-transcribe meetings, extract action items, summarize decisions — from Zoom/Meet to Notion in one workflow.

## What It Does

Captures meeting audio/video → Whisper transcription → LLM summarization → structured notes → distribution.

## Core Capabilities

- **Live Transcription**: Real-time STT via Whisper API
- **Speaker Diarization**: Identify who's speaking (Zoom, Meet, Teams)
- **Action Item Extraction**: Pull tasks, owners, due dates from conversation
- **Decision Log**: Track decisions made with context and rationale
- **Auto Distribution**: Send notes to Notion, Confluence, Slack, email

## Supported Platforms

- Zoom (via webhook recording upload)
- Google Meet (via participant recording)
- Microsoft Teams (via Graph API)
- Direct upload (MP3, M4A, WAV, MP4)

## Usage

```bash
# Transcribe audio
python3 meeting_notes.py transcribe --file meeting.mp4 --output ./notes/

# Generate summary
python3 meeting_notes.py summarize --transcript ./notes/transcript.txt --format markdown
```

## n8n Workflow

See `../integrations/ai-meeting-notes-automation/`:
- Recording trigger → download → transcription → LLM summarization → Notion/Slack delivery

> Part of [agent-studio](https://github.com/nima54851/agent-studio) — AI Agent Skills Marketplace

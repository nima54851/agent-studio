# AI Voice Clone Automation

> Clone any voice from audio samples using AI — generate speech in any voice, any language, any tone.

## What It Does

Takes voice reference audio (5–60 seconds) and generates new speech that sounds like the original speaker. Fully automated via n8n + TTS API.

## Core Capabilities

- **Voice Registration**: Upload reference audio → extract voice embedding → store voice profile
- **Text-to-Speech**: Convert any text into the cloned voice
- **Emotion Control**: Adjust tone — neutral, happy, sad, excited, whisper
- **Multi-language**: Cross-language voice cloning (English voice, Chinese speech, etc.)
- **Batch Generation**: Queue multiple scripts → auto-generate audio files

## Usage

```
# Register a new voice
python3 voice_clone.py register --name "my-voice" --audio samples/voice_ref.mp3

# Generate speech
python3 voice_clone.py generate --voice "my-voice" --text "Hello world" --output hello.mp3
```

## n8n Workflow

See `../integrations/ai-voice-clone-automation/` for the full workflow:
- Audio upload → voice extraction → embedding storage → TTS generation → file output

## Tools Required

- **Coqui TTS** or **ElevenLabs API** or **Resemble.ai**
- n8n with Python node
- S3/MinIO for audio storage

## Files

- `SKILL.md` — this file
- `voice_clone.py` — CLI tool for voice registration and generation
- `README.md` — integration guide

> Part of [agent-studio](https://github.com/nima54851/agent-studio) — AI Agent Skills Marketplace

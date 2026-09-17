# Agent Versioning Automation Skill

**Version:** 1.0.0  
**Author:** agent-studio  
**Tags:** agent-automation, versioning, git, changelog  

## Overview

AI-powered agent versioning system that automatically manages semantic versioning, generates changelogs, tags releases, and maintains version history across multiple agent projects.

## Features

- **Semantic Versioning:** Auto-increment major/minor/patch based on commit analysis
- **Changelog Generation:** AI-generated changelogs from commit messages and PR descriptions
- **Multi-Project Tracking:** Version coordination across related agent repositories
- **Release Notes:** Markdown/HTML release notes with breaking change detection
- **Git Tag Management:** Automated tag creation and push

## Architecture

```
commit → AI Analysis → Version Bump Decision → Changelog Update → Git Tag → Release
```

## Usage

```bash
# Analyze and suggest next version
python3 agent_version_manager.py --project ./my-agent --analyze

# Create a new release
python3 agent_version_manager.py --project ./my-agent --release

# Show version history
python3 agent_version_manager.py --project ./my-agent --history
```

## Integration

- Works with any Git repository
- Outputs n8n-compatible JSON for workflow integration
- Supports GitHub Releases API for automated publishing

## n8n Workflow

See `integrations/agent-versioning-automation/n8n-versioning-workflow.json`

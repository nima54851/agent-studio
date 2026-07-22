# AI Test Generator Automation

## What It Does
Automatically generates unit tests, integration tests, and E2E tests from code using AI — reducing test coverage debt without manual effort.

## Triggers
- PR opened/updated → generate tests for changed files
- New feature merged → generate regression test suite
- Manual trigger via n8n webhook
- Scheduled: weekly test coverage audit

## Capabilities
- **Unit test generation**: pytest, jest, JUnit, xUnit from source
- **Integration test scaffolding**: API endpoint test templates with realistic payloads
- **E2E test generation**: Playwright/Cypress from user flow descriptions
- **Mutation testing**: Verify test quality with Stryker/mutmut
- **Coverage gap analysis**: Identify untested branches, edge cases
- **Flaky test detection**: Track test reliability over time
- **Test data factory**: Auto-generate realistic mock data with Faker.js

## AI Model Support
- Claude Code / GPT-4 / Gemini for test generation
- Configurable assertion style (strict/lenient)
- Language-aware prompts per framework

## Output
- Generated test files committed to `tests/` branch or PR
- Coverage report posted to Slack/Discord
- Test quality score (mutation score > 80% = ✅)

## Setup
```bash
cp -r skills/ai-test-generator-automation $AGENT_SKILLS_DIR/
```

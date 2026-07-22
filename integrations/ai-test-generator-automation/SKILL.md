# AI Test Generator — n8n Integration

## Workflow: Automated Test Generation Pipeline

### Trigger
- GitHub Webhook (PR opened/updated)
- Manual n8n webhook

### Steps
1. **GitHub trigger** → get changed files list
2. **Code filter** → exclude node_modules, dist, test files
3. **AI node** → prompt: "Generate pytest/jest tests for this code"
4. **Test formatter** → fix indentation, imports, assertions
5. **Coverage check** → run pytest --cov / jest --coverage
6. **PR comment** → post test results + coverage delta
7. **Commit** → push generated tests to PR branch

### n8n Nodes
- GitHub Trigger
- Code (file diff parser)
- HTTP Request → Claude API
- Code (test formatter)
- Execute Command (run test suite)
- GitHub node (post comment)
- Slack/Discord (notify)

### Env Vars
- `CLAUDE_API_KEY`
- `GITHUB_TOKEN`
- `TEST_FRAMEWORK` = pytest | jest | mocha

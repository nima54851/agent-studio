# Code Migration — n8n Integration

## Workflow: Automated Framework Migration Pipeline

### Trigger
- GitHub issue labeled `migration`
- Manual n8n webhook with migration config

### Steps
1. **Analyze codebase** → count files, detect framework, list dependencies
2. **Generate migration plan** → AI writes migration script + test updates
3. **Batch conversion** → apply changes in chunks (50 files/batch)
4. **Run tests** → pytest/jest against migrated code
5. **Coverage diff** → compare before/after coverage
6. **Create migration PR** → commit all changes with detailed changelog
7. **Alert team** → Slack/Discord with migration summary

### n8n Nodes
- GitHub Issue Trigger (label filter)
- Code (repo scanner)
- HTTP Request → Claude API (migration plan)
- Code (batch replacer)
- Execute Command (run tests)
- GitHub (create PR)
- Slack (notify team)

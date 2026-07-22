# Code Migration Automation

## What It Does
Automates large-scale code migrations: framework upgrades, language version bumps, library replacements, and architecture refactors — with zero-downtime staged rollout.

## Supported Migrations
| From | To | Status |
|------|-----|--------|
| Python 2 | Python 3 | ✅ |
| AngularJS | Angular 17+ | ✅ |
| React class | React hooks | ✅ |
| jQuery | Vanilla JS | ✅ |
| REST | GraphQL | ✅ |
| Moment.js | date-fns/Luxon | ✅ |
| Webpack | Vite | ✅ |
| Express 4 | Express 5 | ✅ |
| Django 3 | Django 5 | ✅ |
| Ruby 2 | Ruby 3 | ✅ |

## Process
1. **Analysis**: Scan codebase, generate migration map, estimate effort
2. **Batch conversion**: AI-assisted find-replace with safety checks
3. **Test adaptation**: Update broken tests after migration
4. **Validation**: Run full test suite, measure coverage delta
5. **Staged rollout**: Feature flag → gradual traffic shift → full cutover
6. **Rollback plan**: One-click revert if error rate spikes

## Safety Guards
- **Pre-migration backup**: Snapshot before any changes
- **Incremental PRs**: Each migration phase in separate PR
- **Smoke tests**: Critical paths tested after each batch
- **Canary rollout**: 5% → 25% → 100% traffic
- **Error rate monitoring**: Auto-rollback if errors exceed threshold

## Output
- Migration PR with detailed changelog
- Test coverage report (before/after)
- Rollback script
- Monitoring dashboard links

## Setup
```bash
cp -r skills/code-migration-automation $AGENT_SKILLS_DIR/
```

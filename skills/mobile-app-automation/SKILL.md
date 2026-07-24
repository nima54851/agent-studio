# Mobile App Automation

> CI/CD + App Store deployment automation for iOS (Fastlane), Android (Gradle), and cross-platform (React Native / Flutter / Expo).

## What it does

- **iOS**: Fastlane lanes for build, test, sign, and App Store Connect upload
- **Android**: Gradle + Play Console automation via `fastlane supply`
- **Cross-platform**: Expo EAS Build / EAS Submit pipelines
- **AI-assisted**: Auto-generate release notes from commit history, detect screenshots for review, flag crashes before submission
- **Notification**: Slack/Discord alert on build success or failure

## n8n Integration

```json
// integrations/mobile-app-automation/mobile-ci-cd.json
{
  "name": "Mobile CI/CD Pipeline",
  "nodes": [
    {"type": "Trigger", "parameters": {"events": ["push"]}},
    {"type": "Code", "parameters": {"js": "const branch = $json.ref; return [{branch}];", "name": "Detect Branch"}},
    {"type": "HTTP Request", "parameters": {"url": "https://api.github.com/repos/OWNER/REPO/actions/runners"}},
    {"type": "Code", "parameters": {"js": "const sha = $json.head_sha; return [{sha}];", "name": "Get SHA"}},
    {"type": "LLM Chain", "parameters": {"model": "gpt-4", "prompt": "Generate release notes for commits since last release tag"}},
    {"type": "Slack Message", "parameters": {"channel": "#mobile-team", "text": "Build {{ $json.branch }} — Release notes: {{ $json.notes }}"}}
  ]
}
```

## Fastlane Example (iOS)

```ruby
# Fastfile
platform :ios do
  desc "Build and submit to TestFlight"
  lane :beta do
    increment_build_number(xcodeproj: "App.xcodeproj")
    build_app(scheme: "App", export_method: "app-store")
    upload_to_testflight(skip_waiting_for_build_processing: true)
    slack(message: "iOS Beta #{lane_context[SharedValues::BUILD_NUMBER]} uploaded!")
  end

  desc "App Store release"
  lane :release do
    ensure_git_status_clean
    bump_version_type
    build_app(scheme: "App", export_method: "app-store")
    upload_to_app_store(skip_metadata: true, skip_screenshots: true)
    slack(message: "🚀 iOS #{lane_context[SharedValues::VERSION_NUMBER]} live!")
  end
end
```

## Fastlane Example (Android)

```ruby
# Fastfile
platform :android do
  desc "Submit to Play Store internal track"
  lane :internal do
    gradle(task: "assembleRelease")
    supply(track: "internal", aab: "app/build/outputs/apk/release/app-release.aab")
    slack(message: "Android internal build uploaded!")
  end
end
```

## Trigger Examples

| Platform | Trigger | Action |
|---|---|---|
| iOS | Tag pushed | Run `beta` lane |
| Android | PR merged to `main` | Run `internal` lane |
| React Native | Push to `release/*` | Expo EAS Submit |
| Flutter | Release created | Fastlane + Firebase App Distribution |

## Environment Variables

| Variable | Description |
|---|---|
| `FASTLANE_USER` | App Store Connect email |
| `FASTLANE_PASSWORD` | App Store Connect password |
| `MATCH_PASSWORD` | Cert match passphrase |
| `GOOGLE_SERVICES_JSON` | Firebase config (base64) |
| `EAS_BUILD_PROFILE` | Expo build profile |
| `SLACK_WEBHOOK` | Slack incoming webhook |

## Related Skills

- [GitHub Actions Automation](../github-actions-automation/SKILL.md) — for workflow setup
- [CI/CD Testing](../testing-automation/SKILL.md) — for pre-release validation
- [Monitoring & Alerting](../monitoring-alerting-automation/SKILL.md) — for crash alerting

---

*Part of [agent-studio](https://github.com/nima54851/agent-studio) · Auto-generated 2026-07-24*

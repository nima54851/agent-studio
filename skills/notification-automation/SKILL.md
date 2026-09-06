# Notification Automation Skill

## Overview
Unified multi-channel notification system: Email, SMS, Push, Slack, Discord, Telegram. Supports templating, batching, rate limiting, and delivery receipts.

## Features
- **Multi-channel**: Email (SMTP/SendGrid), SMS (Twilio), Push (FCM/APNs), Slack, Discord, Telegram
- **Template engine**: Jinja2-based, supports variables and conditionals
- **Smart batching**: Aggregate notifications, send digests on schedule
- **Rate limiting**: Per-channel throttling to avoid service blocks
- **Delivery tracking**: Webhook receipts, retry on failure, fallback channels
- **Priority levels**: Critical → High → Normal → Low with different delivery paths

## Usage

```json
{
  "channel": "slack",
  "to": "#alerts",
  "template": "incident_alert",
  "data": {
    "service": "payment-api",
    "error": "Stripe timeout",
    "severity": "high"
  },
  "priority": "high"
}
```

## Workflow
```
Trigger → Template Render → Rate Limit Check → Delivery → Receipt → Retry if failed
```

## Priority Mapping
| Priority | Channels | Batch Window |
|----------|----------|--------------|
| Critical | All + SMS | Immediate |
| High | Slack + Email | 5 min |
| Normal | Email | 1 hour |
| Low | Digest | Daily |

## Setup
```bash
npm install notification-hub
# Configure .env with API keys for each channel
```

## n8n Workflow
See `integrations/notification-automation/notification-hub.json`

---

*Skill: notification-automation | v1.0.0 | 2026-09-06*

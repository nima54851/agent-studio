# Product Recommendation Automation

> AI-powered product recommendation engine — collaborative filtering, content-based, and hybrid approaches. A/B test recommendation strategies, track CTR/conversion, and personalize in real time.

## What It Does

- **Collaborative Filtering**: User-item matrix factorization, ALS, KNN-based similarity
- **Content-Based**: TF-IDF / embeddings similarity between product attributes
- **Hybrid**: Weighted combination with contextual bandits for exploration/exploitation
- **A/B Testing**: Multiple strategies in production, real-time CTR + conversion tracking
- **Personalization**: Session-based, user profile, time-of-day, seasonality signals

## Skill Capabilities

- Generate recommendation scores for any product catalog
- Build A/B test pipelines with statistical significance testing
- Connect to Shopify / WooCommerce / custom DB as data source
- Route recommendations via email, push notification, Slack, or webhook
- Weekly digest: top picks per user segment

## Files

- `SKILL.md` — This file
- `recommendation_engine.py` — Core recommendation logic (collaborative + content-based)
- `ab_test_tracker.py` — A/B test runner with statistical significance
- `recommendation_api.py` — FastAPI serving layer with caching

## Setup

```bash
pip install scikit-learn pandas numpy fastapi uvicorn
```

## Usage

```python
from recommendation_engine import HybridRecommender

rec = HybridRecommender(
    collaborative_weight=0.6,
    content_weight=0.4,
    top_k=10
)
recommendations = rec.recommend(user_id="u123", context={"hour": 14, "platform": "web"})
```

## n8n Integration

Import `n8n-recommendation-workflow.json` to connect:
- Shopify/WooCommerce trigger → recommendation engine → personalized email/Slack/push

## OpenClaw Integration

```python
# skill.py
async def recommend_products(context):
    user_id = context.user_id
    context_data = {"hour": context.hour, "platform": context.platform}
    recs = rec.recommend(user_id, context=context_data)
    return {"recommendations": recs}
```

---

*Part of [agent-studio](https://github.com/nima54851/agent-studio) · Built by 灵犀 AI*

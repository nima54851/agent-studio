"""
FastAPI Recommendation Serving API
Caches recommendations and serves them with sub-10ms latency.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import hashlib
import json

from recommendation_engine import HybridRecommender
from ab_test_tracker import ABTestRunner

app = FastAPI(title="Product Recommendation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory cache
_cache: dict = {}
_CACHE_TTL_SECONDS = 300


class RecommendRequest(BaseModel):
    user_id: str
    context: Optional[dict] = None
    top_k: Optional[int] = 10
    exclude_history: bool = True


class RecordEventRequest(BaseModel):
    user_id: str
    product_id: str
    event_type: str  # "impression", "click", "conversion"
    revenue: Optional[float] = None


# Global recommender (initialized on startup)
recommender: Optional[HybridRecommender] = None
ab_test: Optional[ABTestRunner] = None


@app.on_event("startup")
def load_model():
    global recommender, ab_test
    # In production: load from trained model files
    recommender = HybridRecommender(collaborative_weight=0.6, content_weight=0.4)
    # Demo: load sample data
    recommender.fit(
        user_item_matrix={
            "u1": {"p1": 5.0, "p2": 3.0},
            "u2": {"p2": 4.0, "p3": 5.0},
        },
        product_features={
            "p1": {"tags": ["ai", "ml"], "category": "software"},
            "p2": {"tags": ["data", "cloud"], "category": "infrastructure"},
            "p3": {"tags": ["devops", "security"], "category": "infrastructure"},
        },
    )
    ab_test = ABTestRunner("rec-strategy-v1", ["hybrid", "collaborative", "content"], strategy="thompson")
    print("✅ Recommendation model loaded")


@app.get("/health")
def health():
    return {"status": "ok", "model": "hybrid_recommender"}


@app.post("/recommend")
def recommend(req: RecommendRequest):
    """Get personalized product recommendations."""
    # Check cache
    cache_key = hashlib.md5(f"{req.user_id}:{json.dumps(req.context or {})}".encode()).hexdigest()
    if cache_key in _cache:
        return _cache[cache_key]

    # A/B test: select variant
    variant = ab_test.select_variant() if ab_test else "hybrid"

    # Generate recommendations
    recs = recommender.recommend(
        user_id=req.user_id,
        context=req.context or {},
        exclude_history=req.exclude_history,
        top_k=req.top_k or 10,
    )

    # Record impression
    if ab_test:
        ab_test.record_impression(variant, [r["product_id"] for r in recs])

    response = {
        "user_id": req.user_id,
        "variant": variant,
        "recommendations": recs,
        "ab_test_id": ab_test.test_id if ab_test else None,
    }

    # Cache
    _cache[cache_key] = response
    return response


@app.post("/event")
def record_event(req: RecordEventRequest):
    """Record user interaction events."""
    if not ab_test:
        return {"status": "ok"}

    variant = ab_test.select_variant()
    if req.event_type == "impression":
        ab_test.record_impression(variant, [req.product_id])
    elif req.event_type == "click":
        ab_test.record_click(variant)
    elif req.event_type == "conversion":
        ab_test.record_conversion(variant, revenue=req.revenue or 0.0)

    # Also update recommender history
    recommender.record_interaction(req.user_id, req.product_id)

    return {"status": "ok", "event": req.event_type}


@app.get("/ab-test/report")
def ab_report():
    """Get A/B test performance report."""
    if not ab_test:
        raise HTTPException(status_code=404, detail="No active A/B test")
    return ab_test.get_report()


@app.get("/ab-test/significance/{treatment}")
def significance(treatment: str, control: str = "collaborative"):
    """Check statistical significance of a treatment vs control."""
    if not ab_test:
        raise HTTPException(status_code=404, detail="No active A/B test")
    return ab_test.statistical_significance(control, treatment)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

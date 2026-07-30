"""
Hybrid Product Recommendation Engine
Supports collaborative filtering, content-based, and hybrid recommendation strategies.
"""

import json
from typing import Optional
from dataclasses import dataclass
from collections import defaultdict
import random


@dataclass
class RecommendationResult:
    product_id: str
    score: float
    strategy: str  # "collaborative", "content", "hybrid"


class CollaborativeFilter:
    """KNN-based user-item collaborative filtering."""

    def __init__(self, user_item_matrix: dict, k: int = 10):
        self.user_item_matrix = user_item_matrix
        self.k = k
        self._precompute_similarities()

    def _precompute_similarities(self):
        """Precompute cosine similarity between users."""
        self.user_similarities = {}
        users = list(self.user_item_matrix.keys())
        for u1 in users:
            scores = {}
            for u2 in users:
                if u1 == u2:
                    continue
                sim = self._cosine_similarity(
                    self.user_item_matrix.get(u1, {}),
                    self.user_item_matrix.get(u2, {})
                )
                if sim > 0:
                    scores[u2] = sim
            self.user_similarities[u1] = sorted(scores.items(), key=lambda x: -x[1])[:self.k]

    def _cosine_similarity(self, vec1: dict, vec2: dict) -> float:
        common = set(vec1.keys()) & set(vec2.keys())
        if not common:
            return 0.0
        dot = sum(vec1[k] * vec2[k] for k in common)
        norm1 = sum(vec1[k] ** 2 for k in vec1) ** 0.5
        norm2 = sum(vec2[k] ** 2 for k in vec2) ** 0.5
        return dot / (norm1 * norm2 + 1e-9)

    def recommend(self, user_id: str, exclude: set = None, top_k: int = 10) -> list[RecommendationResult]:
        exclude = exclude or set()
        user_ratings = self.user_item_matrix.get(user_id, {})
        neighbors = self.user_similarities.get(user_id, [])

        scores = defaultdict(float)
        for neighbor, similarity in neighbors:
            neighbor_ratings = self.user_item_matrix.get(neighbor, {})
            for product, rating in neighbor_ratings.items():
                if product not in exclude and product not in user_ratings:
                    scores[product] += similarity * rating

        return [
            RecommendationResult(product_id=k, score=round(v, 4), strategy="collaborative")
            for k, v in sorted(scores.items(), key=lambda x: -x[1])[:top_k]
        ]


class ContentBasedFilter:
    """TF-IDF based content similarity."""

    def __init__(self, product_features: dict):
        """
        product_features: {product_id: {"tags": [...], "category": str, "description": str}}
        """
        self.product_features = product_features
        self._build_tfidf_index()

    def _build_tfidf_index(self):
        """Build TF-IDF index from product features."""
        doc_count = len(self.product_features)
        tf = {}
        idf = defaultdict(int)
        all_tokens = set()

        for pid, features in self.product_features.items():
            tokens = self._tokenize(features)
            tf[pid] = tokens
            all_tokens.update(tokens)

        # IDF
        for token in all_tokens:
            idf[token] = sum(1 for pid in self.product_features if token in tf[pid])

        self.idf = {t: (doc_count / (c + 1)) for t, c in idf.items()}
        self.all_tokens = all_tokens

    def _tokenize(self, features: dict) -> set:
        tokens = set()
        if "tags" in features:
            tokens.update(str(t).lower() for t in features["tags"])
        if "category" in features:
            tokens.add(str(features["category"]).lower())
        if "description" in features:
            tokens.update(str(features["description"]).lower().split()[:20])
        return tokens

    def _tfidf_vector(self, tokens: set) -> dict:
        return {t: (1.0 * (1 if t in tokens else 0)) * self.idf.get(t, 0) for t in self.all_tokens}

    def _cosine(self, v1: dict, v2: dict) -> float:
        common = set(v1) & set(v2)
        dot = sum(v1[k] * v2[k] for k in common)
        n1 = sum(v1[k] ** 2 for k in v1) ** 0.5
        n2 = sum(v2[k] ** 2 for k in v2) ** 0.5
        return dot / (n1 * n2 + 1e-9)

    def recommend(self, user_profile: set, exclude: set = None, top_k: int = 10) -> list[RecommendationResult]:
        exclude = exclude or set()
        profile_vec = self._tfidf_vector(user_profile)
        results = []
        for pid, features in self.product_features.items():
            if pid in exclude:
                continue
            tokens = self._tokenize(features)
            score = self._cosine(profile_vec, self._tfidf_vector(tokens))
            if score > 0:
                results.append(RecommendationResult(product_id=pid, score=round(score, 4), strategy="content"))
        return sorted(results, key=lambda x: -x.score)[:top_k]


class HybridRecommender:
    def __init__(self, collaborative_weight: float = 0.6, content_weight: float = 0.4, top_k: int = 10):
        self.collab_weight = collaborative_weight
        self.content_weight = content_weight
        self.top_k = top_k
        self.collab: Optional[CollaborativeFilter] = None
        self.content: Optional[ContentBasedFilter] = None
        self.exclude_history: dict[str, set] = defaultdict(set)

    def fit(self, user_item_matrix: dict, product_features: dict):
        """Train the hybrid model."""
        self.collab = CollaborativeFilter(user_item_matrix)
        self.content = ContentBasedFilter(product_features)

    def recommend(
        self, user_id: str, context: dict = None, exclude_history: bool = True, top_k: int = None
    ) -> list[dict]:
        """Generate hybrid recommendations for a user."""
        top_k = top_k or self.top_k
        context = context or {}
        exclude = self.exclude_history[user_id] if exclude_history else set()

        collab_recs = self.collab.recommend(user_id, exclude=exclude, top_k=top_k * 2) if self.collab else []
        content_recs = self.content.recommend(
            user_profile=context.get("profile_tags", set()), exclude=exclude, top_k=top_k * 2
        ) if self.content else []

        collab_map = {r.product_id: r.score for r in collab_recs}
        content_map = {r.product_id: r.score for r in content_recs}
        all_products = set(collab_map) | set(content_map)

        hybrid_scores = {}
        max_c = max(collab_map.values()) if collab_map else 1
        max_t = max(content_map.values()) if content_map else 1

        for pid in all_products:
            c = (collab_map.get(pid, 0) / max_c) * self.collab_weight if collab_map else 0
            t = (content_map.get(pid, 0) / max_t) * self.content_weight if content_map else 0
            hybrid_scores[pid] = round(c + t, 4)

        sorted_recs = sorted(hybrid_scores.items(), key=lambda x: -x[1])[:top_k]
        return [
            {
                "product_id": pid,
                "score": score,
                "rank": i + 1,
                "user_id": user_id,
                "context": context,
            }
            for i, (pid, score) in enumerate(sorted_recs)
        ]

    def record_interaction(self, user_id: str, product_id: str, rating: float = 1.0):
        """Record a user interaction for future recommendations."""
        self.exclude_history[user_id].add(product_id)


if __name__ == "__main__":
    # Demo
    sample_matrix = {
        "u1": {"p1": 5.0, "p2": 3.0, "p3": 4.0},
        "u2": {"p2": 4.0, "p3": 5.0, "p4": 2.0},
        "u3": {"p1": 3.0, "p4": 5.0, "p5": 4.0},
    }
    sample_features = {
        "p1": {"tags": ["tech", "ai"], "category": "software"},
        "p2": {"tags": ["data", "ml"], "category": "software"},
        "p3": {"tags": ["cloud", "devops"], "category": "infrastructure"},
        "p4": {"tags": ["security", "devops"], "category": "infrastructure"},
        "p5": {"tags": ["product", "ux"], "category": "design"},
    }

    rec = HybridRecommender(collaborative_weight=0.6, content_weight=0.4)
    rec.fit(sample_matrix, sample_features)
    results = rec.recommend("u1", context={"profile_tags": {"ai", "ml"}})
    print("Recommendations for u1:", json.dumps(results, indent=2))

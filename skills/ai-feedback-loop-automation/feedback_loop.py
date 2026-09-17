#!/usr/bin/env python3
"""
AI Feedback Loop - Continuous agent improvement system
"""
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict

class FeedbackLoop:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.outputs = []
        self.feedbacks = {}
        self.scores = defaultdict(list)
    
    def record_output(self, prompt, response, context=None):
        entry = {
            "id": f"{self.agent_id}_{len(self.outputs)}",
            "prompt": prompt,
            "response": response,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
            "quality_score": self._score_output(response)
        }
        self.outputs.append(entry)
        self.scores["quality"].append(entry["quality_score"])
        return entry["id"]
    
    def _score_output(self, response):
        score = 70
        if len(response) > 50:
            score += 10
        if any(marker in response.lower() for marker in ["however", "therefore", "furthermore"]):
            score += 5
        if "error" in response.lower() or "sorry" in response.lower():
            score -= 15
        return min(100, max(0, score))
    
    def collect_feedback(self, response_id, rating, comment=None):
        self.feedbacks[response_id] = {
            "rating": rating,
            "comment": comment,
            "timestamp": datetime.now().isoformat()
        }
        self.scores["satisfaction"].append(rating)
    
    def analyze_and_improve(self):
        if not self.outputs:
            return {"status": "no_data"}
        
        avg_quality = sum(self.scores["quality"]) / len(self.scores["quality"])
        avg_satisfaction = (
            sum(self.scores["satisfaction"]) / len(self.scores["satisfaction"])
            if self.scores["satisfaction"] else None
        )
        
        # Find worst-scoring outputs for pattern analysis
        low_score = [o for o in self.outputs if o["quality_score"] < 60]
        
        return {
            "agent_id": self.agent_id,
            "total_outputs": len(self.outputs),
            "avg_quality_score": round(avg_quality, 1),
            "avg_satisfaction": round(avg_satisfaction, 1) if avg_satisfaction else None,
            "patterns_to_improve": len(low_score),
            "recommendations": self._generate_recommendations(low_score)
        }
    
    def _generate_recommendations(self, low_score_outputs):
        recs = []
        if len(low_score_outputs) > 0:
            recs.append("Consider adding more context to prompt templates")
            recs.append("Review responses flagged for brevity or unclear language")
        return recs


if __name__ == "__main__":
    loop = FeedbackLoop("test-agent")
    rid = loop.record_output("Hello", "Hi! How can I help you?")
    loop.collect_feedback(rid, 4, "Quick and helpful")
    print(json.dumps(loop.analyze_and_improve(), indent=2))

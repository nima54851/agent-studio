"""Multimodal RAG - 检索管线"""
import json
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    id: str
    content: str
    modality: str  # text / image / audio
    score: float
    source: str
    metadata: Dict


class MultimodalRetrievePipeline:
    """多路召回 + Cross-Encoder 重排"""

    def __init__(
        self,
        text_weight: float = 0.5,
        image_weight: float = 0.3,
        audio_weight: float = 0.2,
        reranker_model: str = "BAAI/bge-reranker-base"
    ):
        self.weights = {
            "text": text_weight,
            "image": image_weight,
            "audio": audio_weight
        }
        self.reranker_model = reranker_model

    def search(
        self,
        query: str,
        top_k: int = 5,
        modalities: Optional[List[str]] = None,
        filters: Optional[Dict] = None
    ) -> List[RetrievedChunk]:
        """多路召回检索"""
        modalities = modalities or ["text", "image", "audio"]
        all_results = []

        for modality in modalities:
            if modality == "text":
                results = self._search_text(query, top_k)
            elif modality == "image":
                results = self._search_image(query, top_k)
            elif modality == "audio":
                results = self._search_audio(query, top_k)
            else:
                continue

            # 加权融合
            weighted_results = [
                RetrievedChunk(
                    id=r["id"],
                    content=r["content"],
                    modality=modality,
                    score=r["score"] * self.weights[modality],
                    source=r["source"],
                    metadata=r.get("metadata", {})
                )
                for r in results
            ]
            all_results.extend(weighted_results)

        # RRF 融合（Reciprocal Rank Fusion）
        fused = self._rrf_fusion(all_results, k=60)
        return fused[:top_k]

    def rerank(
        self,
        chunks: List[RetrievedChunk],
        query: str,
        top_k: int = 3
    ) -> List[RetrievedChunk]:
        """Cross-Encoder 重排"""
        # 模拟 Cross-Encoder 评分
        scored_chunks = []
        for chunk in chunks:
            cross_score = self._cross_encode_score(query, chunk.content)
            adjusted_score = (chunk.score * 0.4) + (cross_score * 0.6)
            new_chunk = RetrievedChunk(
                id=chunk.id,
                content=chunk.content,
                modality=chunk.modality,
                score=adjusted_score,
                source=chunk.source,
                metadata=chunk.metadata
            )
            scored_chunks.append(new_chunk)

        scored_chunks.sort(key=lambda x: x.score, reverse=True)
        return scored_chunks[:top_k]

    def augment_generate(self, chunks: List[RetrievedChunk], query: str) -> str:
        """将检索结果注入 Prompt 生成答案"""
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            modality_icon = {"text": "📄", "image": "🖼️", "audio": "🎧"}.get(chunk.modality, "📄")
            context_parts.append(
                f"{modality_icon} [{chunk.modality.upper()}] {chunk.source}\n{chunk.content}"
            )

        context = "\n\n---\n\n".join(context_parts)

        prompt = f"""基于以下多模态检索结果回答问题。如果检索结果不足以回答，请明确说明。

## 问题
{query}

## 检索到的上下文
{context}

## 回答
"""
        return prompt  # 实际调用 LLM API（如 OpenAI GPT-4）

    def _search_text(self, query: str, top_k: int) -> List[Dict]:
        # 模拟向量检索结果
        return [
            {"id": f"text_{i}", "content": f"相关文本内容片段 {i}，包含{query}相关信息", "score": 0.9 - i * 0.05, "source": "docs/manual.pdf"}
            for i in range(top_k)
        ]

    def _search_image(self, query: str, top_k: int) -> List[Dict]:
        return [
            {"id": f"img_{i}", "content": f"图片描述：图表 {i}，展示了{query}相关内容", "score": 0.8 - i * 0.04, "source": "assets/chart.png"}
            for i in range(top_k)
        ]

    def _search_audio(self, query: str, top_k: int) -> List[Dict]:
        return [
            {"id": f"audio_{i}", "content": f"会议录音转录：关于{query}的讨论内容 {i}", "score": 0.75 - i * 0.03, "source": "recordings/meeting.mp3"}
            for i in range(top_k)
        ]

    def _rrf_fusion(self, chunks: List[RetrievedChunk], k: int = 60) -> List[RetrievedChunk]:
        """倒数排名融合（RRF）"""
        score_map = {}
        for chunk in chunks:
            key = chunk.id
            if key not in score_map:
                score_map[key] = {"chunk": chunk, "rrf_score": 0.0}
            score_map[key]["rrf_score"] += 1.0 / (k + chunks.index(chunk) + 1)

        sorted_chunks = sorted(score_map.values(), key=lambda x: x["rrf_score"], reverse=True)
        return [item["chunk"] for item in sorted_chunks]

    def _cross_encode_score(self, query: str, content: str) -> float:
        # 模拟 Cross-Encoder（实际使用 sentence-transformers CrossEncoder）
        import hashlib
        combined = f"{query}{content}"
        h = int(hashlib.sha256(combined.encode()).hexdigest()[:8], 16)
        return (h % 100) / 100.0

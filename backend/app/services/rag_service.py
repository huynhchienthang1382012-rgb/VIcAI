from pathlib import Path
from dataclasses import dataclass
import math

from openai import OpenAI

from app.core.config import get_settings


@dataclass
class Chunk:
    text: str
    source: str
    embedding: list[float]


class RagService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = OpenAI(api_key=self.settings.openai_api_key) if self.settings.openai_api_key else None
        self.chunks: list[Chunk] = []

    def load_knowledge_base(self) -> None:
        kb_path = Path(self.settings.knowledge_path)
        if not kb_path.exists() or not self.client:
            return
        for file in kb_path.glob("*.md"):
            text = file.read_text(encoding="utf-8")
            for paragraph in [p.strip() for p in text.split("\n\n") if p.strip()]:
                emb = self._embed(paragraph)
                self.chunks.append(Chunk(text=paragraph, source=file.name, embedding=emb))

    def _embed(self, text: str) -> list[float]:
        if not self.client:
            return [0.0]
        response = self.client.embeddings.create(model=self.settings.embeddings_model, input=text)
        return response.data[0].embedding

    def _cosine_similarity(self, v1: list[float], v2: list[float]) -> float:
        if len(v1) != len(v2):
            return 0
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0 or norm2 == 0:
            return 0
        return dot / (norm1 * norm2)

    def retrieve(self, query: str, top_k: int = 3) -> list[dict]:
        if not self.client or not self.chunks:
            return []
        q_emb = self._embed(query)
        scored = sorted(
            self.chunks,
            key=lambda c: self._cosine_similarity(q_emb, c.embedding),
            reverse=True,
        )[:top_k]
        return [{"content": c.text, "source": c.source} for c in scored]


rag_service = RagService()

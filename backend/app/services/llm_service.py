from collections.abc import Generator
from openai import OpenAI

from app.core.config import get_settings
from app.services.prompt_router import resolve_model_for_mode, resolve_system_prompt
from app.services.tool_service import TOOLS


class LLMService:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def _try_tool_call(self, user_message: str) -> str | None:
        if user_message.startswith("calc:"):
            exp = user_message.replace("calc:", "", 1).strip()
            return f"Kết quả: {TOOLS['calculator']['handler'](exp)}"
        if "bây giờ là mấy giờ" in user_message.lower():
            return f"Thời gian hiện tại: {TOOLS['current_time']['handler']()}"
        return None

    def stream_answer(
        self,
        mode: str,
        conversation: list[dict],
        retrieved_context: list[dict],
        user_preferences: dict,
    ) -> Generator[str, None, None]:
        tool_result = self._try_tool_call(conversation[-1]["content"])
        if tool_result:
            yield tool_result
            return

        if not self.client:
            yield "[Fallback] Chưa cấu hình OPENAI_API_KEY. Vui lòng thêm key để kích hoạt AI model thực thụ."
            return

        context_text = "\n".join([f"- ({c['source']}) {c['content']}" for c in retrieved_context])
        pref_text = ", ".join([f"{k}: {v}" for k, v in user_preferences.items()]) or "không có"

        messages = [{"role": "system", "content": resolve_system_prompt(mode)}]
        messages.append(
            {
                "role": "system",
                "content": f"Sở thích người dùng: {pref_text}. Nếu thiếu dữ kiện, hãy hỏi lại ngắn gọn. Ngữ cảnh RAG:\n{context_text}",
            }
        )
        messages.extend(conversation)

        stream = self.client.chat.completions.create(
            model=resolve_model_for_mode(mode),
            messages=messages,
            temperature=0.4,
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content or ""
            if delta:
                yield delta


llm_service = LLMService()

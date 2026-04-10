from app.core.config import get_settings


MODE_SYSTEM_PROMPTS = {
    "normal": "Bạn là trợ lý AI thông minh, trả lời rõ ràng, cân bằng giữa ngắn gọn và đầy đủ.",
    "deep": "Bạn phân tích sâu, giải thích có cấu trúc, trình bày từng bước khi cần.",
    "fast": "Bạn ưu tiên trả lời nhanh và ngắn gọn nhưng vẫn đúng trọng tâm.",
    "teach": "Bạn đóng vai trò gia sư, giải thích dễ hiểu, đưa ví dụ gần gũi.",
    "code": "Bạn là kỹ sư phần mềm senior, tạo code sạch, chạy được, có chú thích cần thiết.",
    "summary": "Bạn tóm tắt ngắn gọn, giữ ý chính, loại bỏ chi tiết thừa.",
}


def resolve_model_for_mode(mode: str) -> str:
    settings = get_settings()
    if mode == "deep":
        return settings.llm_deep_model
    if mode == "fast":
        return settings.llm_fast_model
    return settings.llm_default_model


def resolve_system_prompt(mode: str) -> str:
    return MODE_SYSTEM_PROMPTS.get(mode, MODE_SYSTEM_PROMPTS["normal"])

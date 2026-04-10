from dataclasses import dataclass


@dataclass
class GuardrailResult:
    allowed: bool
    message: str | None = None


BLOCKED_PATTERNS = [
    "how to make bomb",
    "steal password",
    "malware source code",
]


def validate_user_input(text: str) -> GuardrailResult:
    lowered = text.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in lowered:
            return GuardrailResult(False, "Xin lỗi, mình không thể hỗ trợ yêu cầu này vì lý do an toàn.")
    if len(text) > 18000:
        return GuardrailResult(False, "Nội dung quá dài, bạn vui lòng chia nhỏ câu hỏi nhé.")
    return GuardrailResult(True)

import json
from fastapi import APIRouter, Depends, HTTPException
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.orm import Session

from app.db.models import Conversation, User
from app.db.session import get_db
from app.schemas.chat import MessageIn
from app.services.auth_service import get_current_user
from app.services.guardrails import validate_user_input
from app.services.llm_service import llm_service
from app.services.memory_service import memory_service
from app.services.rag_service import rag_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/{conversation_id}/stream")
def stream_chat(
    conversation_id: int,
    payload: MessageIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    convo = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == user.id).first()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")

    check = validate_user_input(payload.content)
    if not check.allowed:
        raise HTTPException(status_code=400, detail=check.message)

    memory_service.save_message(db, conversation_id, "user", payload.content)
    history = memory_service.get_recent_messages(db, conversation_id, limit=24)
    conversation_messages = [{"role": m.role, "content": m.content} for m in history]

    references = rag_service.retrieve(payload.content)
    user_preferences = memory_service.get_user_preferences(user)

    def event_generator():
        answer_parts = []
        for token in llm_service.stream_answer(payload.mode, conversation_messages, references, user_preferences):
            answer_parts.append(token)
            yield {"event": "token", "data": token}

        final_text = "".join(answer_parts)
        memory_service.save_message(db, conversation_id, "assistant", final_text)
        yield {"event": "meta", "data": json.dumps({"done": True, "references": references}, ensure_ascii=False)}

    return EventSourceResponse(event_generator())

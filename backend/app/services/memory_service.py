import json
from sqlalchemy.orm import Session

from app.db.models import Message, Conversation, User


class MemoryService:
    def get_recent_messages(self, db: Session, conversation_id: int, limit: int = 20) -> list[Message]:
        return (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
            .all()[::-1]
        )

    def save_message(self, db: Session, conversation_id: int, role: str, content: str) -> Message:
        message = Message(conversation_id=conversation_id, role=role, content=content)
        db.add(message)
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            conversation.updated_at = message.created_at
        db.commit()
        db.refresh(message)
        return message

    def remember_user_preference(self, db: Session, user: User, key: str, value: str) -> None:
        current = json.loads(user.preferences or "{}")
        current[key] = value
        user.preferences = json.dumps(current, ensure_ascii=False)
        db.commit()

    def get_user_preferences(self, user: User) -> dict:
        return json.loads(user.preferences or "{}")


memory_service = MemoryService()

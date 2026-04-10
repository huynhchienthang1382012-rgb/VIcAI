from datetime import datetime
from pydantic import BaseModel


class MessageIn(BaseModel):
    content: str
    mode: str = "normal"


class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime


class ConversationOut(BaseModel):
    id: int
    title: str
    mode: str
    updated_at: datetime


class ConversationCreate(BaseModel):
    title: str = "Cuộc hội thoại mới"
    mode: str = "normal"

from datetime import datetime

from pydantic import BaseModel


class ChatBase(BaseModel):
    id: str
    name: str


class ChatCreate(ChatBase):
    pass


class ChatUpdate(BaseModel):
    name: str
    updated_at: datetime


class ChatResponse(ChatBase):
    pass


class ChatListResponse(ChatBase):
    pass

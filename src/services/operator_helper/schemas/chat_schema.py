from pydantic import BaseModel


class ChatBase(BaseModel):
    id: str
    name: str


class ChatCreate(ChatBase):
    pass


class ChatUpdate(ChatBase):
    name: str


class ChatResponse(ChatBase):
    pass


class ChatListResponse(ChatBase):
    pass

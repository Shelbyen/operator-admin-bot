from pydantic import BaseModel


class ChatBase(BaseModel):
    id: int
    name: str


class ChatCreate(ChatBase):
    pass


class ChatUpdate(ChatBase):
    id: None


class ChatResponse(ChatBase):
    pass


class ChatListResponse(ChatBase):
    pass

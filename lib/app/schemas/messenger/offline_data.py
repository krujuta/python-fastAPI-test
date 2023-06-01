# To store offline data for chats in messanger

from pydantic import BaseModel
from typing import Optional


class OfflineDataBase(BaseModel):
    company: str = ""
    sender_id: int = 0
    receiver_id: int = 0
    content: str = ""
    date: str = ""
    content_type: str = ""


# Properties to receive on item creation
class OfflineDataCreate(OfflineDataBase):
    company: str = ""
    sender_id: int = 0
    receiver_id: int = 0
    content: str = ""
    date: str = ""
    content_type: str = ""


# Properties to receive on item update
class OfflineDataUpdate(OfflineDataBase):
    content: str = ""
    date: str = ""
    content_type: str = ""
    pass


# Properties shared by models stored in DB
class OfflineDataInDBBase(OfflineDataBase):
    id: Optional[int]
    company: str = ""
    sender_id: int = 0
    receiver_id: int = 0
    content: str = ""
    date: str = ""
    content_type: str = ""

    class Config:
        orm_mode = True


# Properties to return to client
class OfflineData(OfflineDataInDBBase):
    id: int
    company: str = ""
    sender_id: int = 0
    receiver_id: int = 0
    content: str = ""
    date: str = ""
    content_type: str = ""
    pass


# Properties stored in DB
class OfflineDataInDB(OfflineDataInDBBase):
    pass

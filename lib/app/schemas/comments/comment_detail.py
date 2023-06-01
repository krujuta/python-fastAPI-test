from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

from lib.app.schemas.base_users import BaseUser
from lib.app.schemas.my_services import ServiceStatus


class CommentDetailBase(BaseModel):
    comment: Optional[str] = ""
    timestamp: Optional[datetime] = ""
    created_user_id: Optional[str] = ""
    company_profile_id: Optional[str] = ""
    service_detail_id: Optional[str] = ""
    service_status_id: Optional[str] = ""
    service_status: Optional[ServiceStatus] = ""
    created_user_profile: Optional[BaseUser] = ""


# Properties to receive on item creation
class CommentDetailCreate(CommentDetailBase):
    comment: Optional[str] = ""
    timestamp: Optional[datetime] = ""
    created_user_id: Optional[str] = ""
    company_profile_id: Optional[str] = ""
    service_detail_id: Optional[str] = ""
    service_status_id: Optional[str] = ""
    pass


# Properties to receive on item update
class CommentDetailUpdate(CommentDetailBase):
    pass


# Properties shared by models stored in DB
class CommentDetailInDBBase(CommentDetailBase):
    id: Optional[str]

    class Config:
        orm_mode = True


# Properties to return to client
class CommentDetail(CommentDetailInDBBase):
    comment: Optional[str] = ""
    timestamp: Optional[datetime] = ""
    created_user_id: Optional[str] = ""
    company_profile_id: Optional[str] = ""
    service_detail_id: Optional[str] = ""
    service_status_id: Optional[str] = ""
    service_status: Optional[ServiceStatus] = ""
    created_user_profile: Optional[BaseUser] = ""
    pass


# Properties stored in DB
class CommentDetailInDB(CommentDetailInDBBase):
    pass

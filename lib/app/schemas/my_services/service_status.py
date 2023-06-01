from pydantic import BaseModel
from typing import Optional
from lib.app.schemas.my_services.service_detail import ServiceDetail
from lib.app.schemas.base_users.base_user import BaseUser


class ServiceStatusBase(BaseModel):
    service_detail_id: Optional[str]
    status: Optional[str] = ""
    service_provider_id: Optional[str]


# Properties to receive on item creation
class ServiceStatusCreate(ServiceStatusBase):
    service_detail_id: Optional[str]
    status: Optional[str] = ""
    processed_by_user_id: Optional[str]


# Properties to receive on item update
class ServiceStatusUpdate(ServiceStatusBase):
    service_detail_id: Optional[str]
    status: Optional[str] = ""
    request_for_serviceprovider: Optional[bool] = False  # used in API call for determining request queue
    request_for_machineuser: Optional[bool] = False     # used in API call for determining request queue
    pass


# Properties shared by models stored in DB
class ServiceStatusInDBBase(ServiceStatusBase):
    id: Optional[str]
    service_detail_id: Optional[str]
    service_provider_id: Optional[str]

    class Config:
        orm_mode = True


# Properties to return to client
class ServiceStatus(ServiceStatusInDBBase):
    processed_by_user_id: Optional[str]
    service_details: Optional[ServiceDetail]
    processed_by_user: Optional[BaseUser]

    pass


# Properties stored in DB
class ServiceStatusInDB(ServiceStatusInDBBase):
    pass


# Properties for post call
class ServiceStatusPost(ServiceStatusInDBBase):
    pass



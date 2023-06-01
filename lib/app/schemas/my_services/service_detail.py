from pydantic import BaseModel
from typing import Optional, Any

from lib.app.schemas.my_services.category import Category
from ..base_users.company_profile import CompanyProfile


class ServiceDetailBase(BaseModel):
    address: Optional[str] = ""
    created_date: Optional[str] = ""
    price: Optional[int] = 0


# Properties to receive on item creation
class ServiceDetailCreate(ServiceDetailBase):
    address: str = ""
    created_user_id: str = ""
    machine_oem_id: str = ""
    machine_type_id: str = ""
    machine_series_id: str = ""
    controller_oem_id: str = ""
    time_window_for_execution_id: Optional[str] = ""
    category_id: Optional[str]
    company_profile_id: int
    note: Optional[str] = ""
    request_for_serviceprovider: Optional[bool] = False  # used in API call for determining request queue
    request_for_machineuser: Optional[bool] = False     # used in API call for determining request queue
    created_date: Optional[str] = ""
    price: Optional[int] = 0


# Properties to receive on item update
class ServiceDetailUpdate(ServiceDetailBase):
    request_for_serviceprovider: Optional[bool] = False  # used in API call for determining request queue
    request_for_machineuser: Optional[bool] = False     # used in API call for determining request queue
    pass


class ServiceDetailStatusUpdate(ServiceDetailBase):
    pass


# Properties shared by models stored in DB
class ServiceDetailInDBBase(ServiceDetailBase):
    id: Optional[str]

    class Config:
        orm_mode = True


# Properties to return to client
class ServiceDetail(ServiceDetailInDBBase):
    category: Optional[Category]
    category_id: Optional[str]
    created_user_id: Optional[str]
    company_profile: Optional[CompanyProfile] = ""
    company_profile_id: str = "" 
    note: Optional[str] = ""
    pass


# Properties stored in DB
class ServiceDetailInDB(ServiceDetailInDBBase):
    pass


class ServiceDetailView(ServiceDetail):
    address: str = ""
    service_detail_id : str = ""
    service_provider_id: str = ""
    status: str = ""
    processed_by_user_id: str = ""
    created_user_id: str = ""
    machine_oem_id: str = ""
    machine_type_id: str = ""
    machine_series_id: str = ""
    controller_oem_id: str = ""
    time_window_for_execution_id: str = ""

    company_name: str = ""
    type_of_machine: str = ""
    machine_manufacturers: str = ""
    control_manufactor_series: str = ""
    request_for_serviceprovider: str = ""
    request_for_user: str = ""

    category_id: Optional[str] = ""
    category: Optional[Category]

    company_profile_id: str = ""
    company_profile: Optional[CompanyProfile] = "" 
    note: Optional[str] = ""
    price: Optional[int] = 0
    pass

from pydantic import BaseModel
from typing import Optional, Any


class MachineDetailBase(BaseModel):
    machine: Optional[str] = ""
    machine_type_id: Optional[str] = ""
    construction_year: Optional[str] = ""
    created_user_id: Optional[str] = ""
    company_profile_id: Optional[str] = ""


# Properties to receive on item creation
class MachineDetailCreate(MachineDetailBase):
    machine_oem_id: Optional[str] = ""
    machine_type_id: Optional[str] = ""
    construction_year: Optional[str] = ""
    created_user_id: Optional[str] = ""
    company_profile_id: Optional[str] = ""
    pass


# Properties to receive on item update
class MachineDetailUpdate(MachineDetailBase):
    pass


# Properties shared by models stored in DB
class MachineDetailInDBBase(MachineDetailBase):
    id: Optional[str]

    class Config:
        orm_mode = True


# Properties to return to client
class MachineDetail(MachineDetailInDBBase):
    machine_oem_id: Optional[str] = ""
    machine_type_id: Optional[str] = ""
    machine_series_id: Optional[str] = ""
    controller_oem_id: Optional[str] = ""
    time_window_for_execution_id: Optional[str] = ""
    created_user_id: Optional[str] = ""
    company_profile_id: str = ""
    machine_type: Optional[str] = ""

    pass


# Properties stored in DB
class MachineDetailInDB(MachineDetailInDBBase):
    pass

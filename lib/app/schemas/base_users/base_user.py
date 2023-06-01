# Base user

from .company_profile import CompanyProfile
from pydantic import BaseModel, EmailStr
from typing import Optional


class BaseUserBase(BaseModel):
    name: str = ""
    job_title: Optional[str] = ""
    phone_number: str = ""
    email: Optional[EmailStr] = ""
    is_admin: Optional[bool] = False
    is_normal_user: Optional[bool] = False
    company_profile_id: Optional[str] = ""
    image_url: Optional[str] = ""


# Properties to receive on item creation
class BaseUserCreate(BaseUserBase):
    name: str = ""
    job_title: str = ""
    phone_number: str = ""
    email: str = ""
    is_admin: Optional[bool] = False
    is_normal_user: Optional[bool] = False
    company_profile_id: Optional[str] = ""
    is_service_provider: Optional[bool] = False
    is_machine_user: Optional[bool] = False
    image_url: Optional[str] = ""


# Properties to receive on item update
class BaseUserUpdate(BaseUserBase):
    name: Optional[str] = ""
    job_title: Optional[str] = ""
    is_admin: Optional[bool] = False
    is_normal_user: Optional[bool] = False
    is_service_provider: Optional[bool] = False
    is_machine_user: Optional[bool] = False
    pass


# Properties shared by models stored in DB
class BaseUserInDBBase(BaseUserBase):
    id: Optional[str]
    company_profile_id: Optional[str]

    class Config:
        orm_mode = True


# Properties to return to client
class BaseUser(BaseUserInDBBase):
    is_service_provider: Optional[bool] = False
    is_machine_user: Optional[bool] = False
    company_profile: Optional[CompanyProfile] = None

    pass


# Properties stored in DB
class BaseUserInDB(BaseUserInDBBase):
    pass

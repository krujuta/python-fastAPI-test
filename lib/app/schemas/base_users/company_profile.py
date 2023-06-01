from pydantic import BaseModel, EmailStr
from typing import Optional, List


class CompanyProfileBase(BaseModel):
    company_name: str = ""
    company_address: Optional[str] = ""
    phone_number: str = ""
    email: Optional[EmailStr] = ""
    description: Optional[str] = ""
    is_service_provider: Optional[bool] = False
    is_machine_user: Optional[bool] = False
    image_url: Optional[str] = ""


# Properties to receive on item creation
class CompanyProfileCreate(CompanyProfileBase):
    company_name: str = ""
    company_address: Optional[str] = ""
    phone_number: str = ""
    email: Optional[EmailStr] = ""
    description: Optional[str] = ""
    is_service_provider: Optional[bool] = False
    is_machine_user: Optional[bool] = False
    image_url: Optional[str] = ""


# Properties to receive on item update
class CompanyProfileUpdate(CompanyProfileBase):
    company_name: Optional[str] = ""
    company_address: Optional[str] = ""
    phone_number: Optional[str] = ""
    email: Optional[EmailStr] = ""
    description: Optional[str] = ""
    is_service_provider: Optional[bool] = False
    is_machine_user: Optional[bool] = False
    pass


# Properties shared by models stored in DB
class CompanyProfileInDBBase(CompanyProfileBase):
    id: Optional[str]
    company_name: str = ""
    is_service_provider: Optional[bool] = False
    is_machine_user: Optional[bool] = False

    class Config:
        orm_mode = True


# Properties to return to client
class CompanyProfile(CompanyProfileInDBBase):
    pass


# Properties stored in DB
class CompanyProfileInDB(CompanyProfileInDBBase):
    pass

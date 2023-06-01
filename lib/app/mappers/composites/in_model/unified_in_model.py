from pydantic import BaseModel
from typing import Optional, List
from lib.app.schemas.base_users.company_profile import CompanyProfile
from lib.app.schemas.base_users.base_user import BaseUser
from lib.app.schemas.my_services.service_detail import ServiceDetailView
from lib.app.schemas.my_services.service_status import ServiceStatus
from lib.app.schemas.user import User
from lib.app.schemas.machine_management import MachineDetailCreate
from lib.app.schemas.comments import CommentDetailCreate


class UnifiedInModel(BaseModel):
    company_profile: Optional[CompanyProfile] = None
    created_user: Optional[BaseUser] = None
    service_provider: Optional[BaseUser] = None
    processed_by_user: Optional[BaseUser] = None
    service_detail: Optional[ServiceDetailView] = None
    service_status: Optional[ServiceStatus] = None
    user: Optional[List[User]] = None
    machine_detail: Optional[MachineDetailCreate] = None
    comment_detail: Optional[CommentDetailCreate] = None

    class Config:
        orm_mode = True

    pass

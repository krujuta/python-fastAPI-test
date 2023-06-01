from pydantic import BaseModel
from typing import Optional, List

from lib.app.schemas.base_users.company_profile import CompanyProfile
from lib.app.schemas.base_users.base_user import BaseUser
from lib.app.schemas.my_services.service_detail import ServiceDetailView
from lib.app.schemas.my_services.service_status import ServiceStatus
from lib.app.schemas.my_services import Category
from lib.app.schemas.user import User
from lib.app.schemas.machine_management import MachineDetail
from lib.app.schemas.comments import CommentDetail


class UnifiedOutModel(BaseModel):
    company_profiles: Optional[List[CompanyProfile]] = None
    created_users: Optional[List[BaseUser]] = None
    service_providers: Optional[List[BaseUser]] = None
    processed_by_users: Optional[List[BaseUser]] = None
    service_details: Optional[List[ServiceDetailView]] = None
    service_statuses: Optional[List[ServiceStatus]] = None
    category: Optional[List[Category]] = None
    user: Optional[List[User]] = None
    machines: Optional[List[MachineDetail]] = None
    comments: Optional[List[CommentDetail]] = None

    class Config:
        orm_mode = True

    pass

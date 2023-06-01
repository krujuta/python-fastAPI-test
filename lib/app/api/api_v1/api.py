from fastapi import APIRouter

from lib.app.api.api_v1.endpoints.entity import user_helps
from lib.app.api.api_v1.endpoints.messenger import messengers
from lib.app.api.api_v1.endpoints.my_services import services, service_details, service_status
from lib.app.api.api_v1.endpoints.comments import comment_details
from lib.app.api.api_v1.endpoints.machine_management import machine_details
from lib.app.api.api_v1.endpoints.base_users import base_users, company_profiles

api_router = APIRouter()
api_router.include_router(user_helps.router, prefix="/user_helps", tags=["user_utilities"])
api_router.include_router(messengers.router, prefix="/messengers", tags=["messengers"])
api_router.include_router(services.router, prefix="/service_provider", tags=["service_provider_services"])
api_router.include_router(service_details.router, prefix="/service_details", tags=["service_provider_services"])
api_router.include_router(machine_details.router, prefix="/machine_management", tags=["machine_management"])
api_router.include_router(comment_details.router, prefix="/comments_management", tags=["comment_management"])
api_router.include_router(service_status.router, prefix="/service_requests", tags=["services"])
api_router.include_router(base_users.router, prefix="/base_users", tags=["base_users"])
api_router.include_router(company_profiles.router, prefix="/company_profiles", tags=["company_profiles"])


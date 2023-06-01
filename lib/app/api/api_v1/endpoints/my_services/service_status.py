from typing import Any, Optional

from fastapi import APIRouter, status
from sqlalchemy.orm import Session

from lib.app import crud, models, schemas, mappers
from lib.app.api import deps
from lib.app.auth.firebase_auth import AuthInterceptor
from fastapi import Depends

from lib.app.error_handling.exceptions import CustomException

jwt_bearer = AuthInterceptor()
router = APIRouter()


@router.get("/", response_model=mappers.UnifiedOutModel)
def read_service_status(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    # retrieve services status
    if crud.user.is_superuser(current_user):
        service_status = crud.service_status.get_multi(
            db, skip=skip, limit=limit)
    else:
        service_status = crud.service_status.get_multi_by_user_id(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )

    out_model = mappers.UnifiedOutModel()
    if service_status is not None:
        out_model.service_statuses = service_status
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Service Status details not found")


@router.get("/my_requested_services",
            response_model=mappers.UnifiedOutModel,
            response_model_exclude_none=True,
            response_model_exclude_unset=True
            )
def get_my_service_requests_by_user_id(
        *,
        db: Session = Depends(deps.get_db),
        user_id: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    # retrieve requested services by user id
    """
    Retrieve my requested services by user_id
    user_id : the user viewing the service requests. e.g. machine user.
    displays all services with requested, accepted, deleted status
    Screen sequence: technician services -> my services [option selection] -> my scervices page
    Screen : TM_U_MyServices
    """
    user_id = user_id.replace('%', ':')
    service_status = crud.service_status.get_multi_by_user_id(
        db=db, user_id=user_id)
    out_model = mappers.UnifiedOutModel()
    if service_status is not None:
        out_model.service_statuses = service_status
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Service Status details not found for user id: % " % user_id)


@router.get("/my_services_history",
            response_model=mappers.UnifiedOutModel,
            response_model_exclude_none=True,
            response_model_exclude_unset=True
            )
def get_services_history_by_user_id(
        *,
        db: Session = Depends(deps.get_db),
        user_id: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    # retrieve history of services by user id
    """
    Retrieve my requested services by user_id
    user_id : the user viewing the history of service requests. e.g. machine user.
    displays all services with requested, accepted, deleted status
    Screen : TM_U_MyServices
    """
    service_status = crud.service_status.get_multi_by_user_id(
        db=db, user_id=user_id)
    out_model = mappers.UnifiedOutModel()
    if service_status is not None:
        out_model.service_statuses = service_status
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Service Status details not found for user id: %" %user_id)


# Requested inbox for service providers.the service provider then can accept or reject or delete the request
@router.get("/requested_services_inbox",
            response_model=mappers.UnifiedOutModel,
            response_model_exclude_unset=True,
            response_model_exclude_none=True
            )
def get_requested_services_inbox(
        *,
        db: Session = Depends(deps.get_db),
        user_id: str,
        request_status: Optional[str] = None,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
        get services status list for service providers:
        when user requests a service it displays in the service provider's request inbox.
        This API returns list of these requested services by user id which can be displayed to the user
        which can be accepted, rejected or deleted further.
        Screen : TM_U_Requested_inbox

        Screen sequence:

    """
    # retrieve services service_provider_id
    user_id = user_id.replace("%", ":")
    service_requests = crud.service_status.get_multi_by_service_provider_request_status(
        db=db, service_provider_id=user_id, request_status=request_status)
    out_model = mappers.UnifiedOutModel()
    if service_requests is not None:
        out_model.service_statuses = service_requests
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Service Status details not found for given details")


# Requested inbox
# can be used with current_user once the authentication is enabled.
# For now, we will pass user_id to check if the user is service_provider or machine_user
# not in the scope for AMB. Will be enabled afterwards.
# @router.get("/requested_services_inbox",
#             response_model=List[schemas.ServiceStatus],
#             response_model_include=["service_detail_id",
#                                     "status",
#                                     "service_details", "id"],
#             )
# def get_requested_services_by_user_type(
#         *,
#         db: Session = Depends(deps.get_db),
#         user_id: int,
#         request_status: Optional[str] = None,
#         current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#         get services status list by user type :
#         when user requests a service for service provider, machine user it displays in their service request inbox.
#         This API returns list of these requested services by user id which can be displayed to the user
#         which can be accepted, rejected or deleted further.
#         Screen : TM_U_Requested_inbox
#     """
#     # retrieve services by category name filter
#     base_user = crud.base_user.get_by_id(db=db, user_id=user_id)  # to get category id by name
#
#     # get data with user type - serviceprovider and user, will be used in the future.
#     # Not in the scope for AMB
#
#     if base_user is not None:
#         service_requests = crud.service_status.get_multi_by_user_type(db=db,
#                                                                       service_provider=base_user.is_service_provider
#                                                                       , machine_user=base_user.is_machine_user)
#     if base_user is not None and request_status is not None:
#         service_requests = crud.service_status.get_multi_by_user_type_and_status(db=db,
#                                                                                  service_provider=
#                                                                                  base_user.is_service_provider,
#                                                                                  machine_user=
#                                                                                  base_user.is_machine_user,
#                                                                                  request_status=request_status)
#
#     if not service_requests:
#         raise HTTPException(status_code=404, detail="Service Status for requested user type not found")
#     if not crud.user.is_superuser(current_user) and (service_requests.owner_id != current_user.id):
#         raise HTTPException(status_code=400, detail="Not enough permissions")
#     return service_requests

@router.post("/send_service_request", response_model=mappers.UnifiedOutModel)
def send_service_request(
        *,
        db: Session = Depends(deps.get_db),
        service_status_in: mappers.UnifiedInModel,
) -> Any:
    """
    Send service request -  when the service is already created and displayed in service marketplace.
    The user gets the list of services -> check details -> send service request
    The service request is sent to the particular service provider who is offering the service.

    Required fields :
    {
        "service_detail_id": 9,
        "status": "string",
        "processed_by_user_id": 15
    }

    Screen: TM_U_Servicea_Detail
    """
    service_status_in = service_status_in.service_detail

    service_status_in = {"service_detail_id": service_status_in.service_detail_id,
                         "status": service_status_in.status, "processed_by_user_id": service_status_in.processed_by_user_id}

    service_detail = crud.service_detail.get_by_service_id(
        db=db, service_id=service_status_in["service_detail_id"])

    if service_detail is not None:
        service_status_in["service_provider_id"] = service_detail.created_user_id

    if service_detail is not None:
        service_status = crud.service_status.create_with_owner(
            db=db, obj_in=service_status_in)
        # if not service_status:
        #     raise HTTPException(
        #         status_code=500,
        #         detail="Unable to create service status to be processed in service status table",
        #     )

    out_model = mappers.UnifiedOutModel()
    if service_status is not None:
        out_model.service_statuses = [service_status]
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error sending service status request")


@router.post("/make_request", response_model=mappers.UnifiedOutModel)
def make_service_status(
        *,
        db: Session = Depends(deps.get_db),
        service_detail_in: mappers.UnifiedInModel,
) -> Any:
    """
    Make service request -  .
    The user makes a service request with the service details - one of the options of home page,
    the request can be made to the machine users or service providers or both
    when selected option -> both : request_for_serviceprovider = true, request_for_machine_user = true,
    company name -> title

    Required fields:
    {
      "company_name": "abc",
      "address": "koblenz",
      "type_of_machine": "mill machine",
      "machine_oem": "chiron",
      "machine_type": "abc",
      "machine_series": "abc",
      "created_user_id": 1,
      "category_id": 1, ---> by default to be assigned to all
      "company_profile_id": 1,
      "note": "string",
      "request_for_serviceprovider": true,
      "request_for_machineuser": false
    }
    """
    service_detail_in = service_detail_in.service_detail

    service_detail_in = {
        "company_profile_id": service_detail_in.company_profile_id,
        "address": "Germany",
        #"machine_type_id": None,
        "created_date": "2022",
        "created_user_id": service_detail_in.created_user_id,
        "category_id": "test:category:2",
        "note": service_detail_in.note,
        "request_for_serviceprovider": service_detail_in.request_for_serviceprovider,
        "request_for_machineuser": service_detail_in.request_for_machineuser
    }
    # 1. create service details
    service_detail = crud.service_detail.create_with_owner(
        db=db, obj_in=service_detail_in)
    out_model = mappers.UnifiedOutModel()
    if service_detail is not None:
        out_model.service_details = [service_detail]
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error making service status request")


@router.put("/update_service_status/{service_status_id}", response_model=mappers.UnifiedOutModel)
def update_service_status(
        *,
        db: Session = Depends(deps.get_db),
        service_status_id: str,
        status_change: str,
) -> Any:
    """
    Update status of the service e.g. Accepted, Completed etc.

    requested : requesting the service - through send request
    accepted : when the service provider accept the request
    deleted : when service provider deletes the request
    completed : when service provider marks the request as completed
    """
    service_status = crud.service_status.get(db, id=service_status_id)
    status_in = schemas.ServiceStatusUpdate()
    # validate status change
    status_in.status = status_change

    service_status = crud.service_status.update(
        db, db_obj=service_status, obj_in=status_in)
    out_model = mappers.UnifiedOutModel()
    if service_status is not None:
        out_model.service_statuses = [service_status]
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error updating service status for id: %" % service_status_id)

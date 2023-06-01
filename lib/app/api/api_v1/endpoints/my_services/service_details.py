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


@router.get("/",
            response_model=mappers.UnifiedOutModel,
            )
def read_service_details(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        category_name: Optional[str] = None,
        machine_type: Optional[str] = None,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    # retrieve services details
    filtered_list = list()
    list_all = crud.service_detail.get_multi(db=db, skip=skip, limit=limit)
    if category_name is not None:
        if category_name == 'Alle':
            filtered_list = list_all
        else:
            category_obj = crud.category.get_by_category(db=db, category=category_name)
            if category_obj:    # not-null
                filtered_list = [x for x in list_all if x.category == category_obj.category]

    # if machine_type is not None:
    #     mt_obj = crud.machine_type.get_by_machine_type(db=db, machine_type=machine_type)
    #     if mt_obj:  # not-null
    #         filtered_list = [x for x in list_all if x.machine_type == mt_obj.id]

    # else:
    #     filtered_list = list_all

    if filtered_list is not None:
        # out_model = mappers.ServiceDetailsMapper.service_details_mapper(db=db, service_details=service_details)
        out_model = mappers.UnifiedOutModel()
        out_model.service_details = filtered_list
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Service details not found for the given details")

    return out_model


@router.get("/{service_id}",
            response_model=mappers.UnifiedOutModel,
            # response_model_exclude_none=True,
            )
def read_service_details_by_id(
        *,
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        service_id: str,
) -> Any:
    # retrieve service details by id
    """
        Screen : TM_U_Servicea_Detail
    """
    service_detail = crud.service_detail.get_by_id(db, id=service_id)

    if service_detail is not None:
        out_model = mappers.UnifiedOutModel()
        out_model.service_details = [service_detail] 
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Service details not found for id: %" % service_id)

    return out_model

 
@router.get("/services/category/{category_id}",
            response_model=mappers.UnifiedOutModel,
            )
def get_services_by_category_id(
        *,
        db: Session = Depends(deps.get_db),
        category: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    # retrieve services by category filter
    category_data = crud.category.get_by_id(db=db, id=category)

    if category_data.category == 'Alle':
        service_details = crud.service_detail.get_multi(db=db)
    else:
        service_details = crud.service_detail.get_multi_by_category(
            db=db, id=category)

    if service_details is not None:
        out_model = mappers.UnifiedOutModel()
        out_model.service_details = service_details 
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Service details not found for category id: %" % category)

    return out_model


# get by category and company profile id
@router.get("/services/{company_profile_id}/{category_id}",
            response_model=mappers.UnifiedOutModel,
            # response_model_exclude_none=True
            )
def get_services_by_comp_id_category_id(
        *,
        db: Session = Depends(deps.get_db),
        category_id: str,
        company_profile_id: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    # retrieve services by category filter

    # get data from database
    category_data = crud.category.get_by_id(db=db, id=category_id)
    if category_data.category == 'Alle':
        service_details = crud.service_detail.get_multi(db=db)
    else:
        service_details = crud.service_detail.get_by_category_comp_profile(db=db, category_id=category_id,
                                                                           company_profile_id=company_profile_id)

    # transform database model to out model
    if service_details is not None:
        out_model = mappers.UnifiedOutModel()
        out_model.service_details = service_details 

        # add company profiles to the response
        company_profile = crud.company_profile.get_by_id(
            db=db, id=company_profile_id)
        company_profiles = list()
        company_profiles.append(company_profile)

        out_model.company_profiles = company_profiles

    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Service details not found for given details")

    return out_model


@router.put("/{id}", response_model=mappers.UnifiedOutModel)
def update_item(
        *,
        db: Session = Depends(deps.get_db),
        service_id: int,
        service_detail_in: schemas.ServiceDetailUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    # update service detail id
    out_model = mappers.UnifiedOutModel()
    service_detail = crud.service_detail.get(db=db, id=service_id)
    if service_detail is not None:
        out_model.service_details = [service_detail]
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error updating service details for id: %" % service_id)


@router.get("/company_name/{company_name}",
            response_model=mappers.UnifiedOutModel,
            response_model_exclude_none=True)
def read_service_detail_comp_name(
        *,
        db: Session = Depends(deps.get_db),
        company_name: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    # retrieve service details by company names

    service_details = crud.service_detail.get_multi_by_company_name(
        db=db, id=company_name)

    company_profile = crud.company_profile.get_by_name(
        db=db, company_name=company_name)

    out_model = mappers.UnifiedOutModel()
    company_profiles = list()

    if service_details is not None or company_profile is not None:  # need to check through ui
        company_profiles.append(company_profile)
        out_model.company_profiles = company_profiles
        out_model.service_details = service_details
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Service details not found for given details")


@router.delete("/{id}", response_model=mappers.UnifiedOutModel)
def delete_service_detail(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    # delete service detail by id

    service_detail = crud.service_detail.get(db=db, id=id)
    out_model = mappers.UnifiedOutModel()

    if service_detail is not None:
        out_model.service_details = [service_detail]
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error deleting service details for id: %" % id)

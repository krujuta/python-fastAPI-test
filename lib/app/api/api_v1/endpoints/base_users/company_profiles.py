from typing import Any, List

from fastapi import APIRouter, status
from sqlalchemy.orm import Session

from lib.app import crud, models, schemas, mappers
from lib.app.api import deps
from lib.app.auth.firebase_auth import AuthInterceptor
from fastapi import Depends

from lib.app.error_handling.exceptions import CustomException

jwt_bearer = AuthInterceptor()
router = APIRouter()


@router.post("/", response_model=mappers.UnifiedOutModel)
def create_company_profile(
        *,
        db: Session = Depends(deps.get_db),
        in_model: mappers.UnifiedInModel,
) -> Any:
    """
    Create new company profile.
    """
    out_model = mappers.UnifiedOutModel()
    company_profile_list = list()
    company_profile = None
    if in_model.company_profile is not None:
        company_profile = crud.base_users.company_profile.create(db, obj_in=in_model.company_profile)
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Database error creating company profile")

    if company_profile is not None:
        company_profile_list.append(company_profile)
        out_model.company_profiles = company_profile_list
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error creating company profile")


@router.put("/update", response_model=mappers.UnifiedOutModel)
def update_company_profile(
        *,
        db: Session = Depends(deps.get_db),
        in_model: mappers.UnifiedInModel,
) -> Any:
    """
    Update a company profile.
    """
    out_model = mappers.UnifiedOutModel()
    company_profile_list = list()
    new_company_profile = None

    if in_model.company_profile is not None:
        try:
            company_user = user = crud.base_users.company_profile.get(db, id=in_model.company_profile.id)

            if company_user is not None:
                new_company_profile = crud.base_users.company_profile.update(db, db_obj=user,
                                                                             obj_in=in_model.company_profile)
        except:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  detail="Database error updating company profile")

    if new_company_profile is not None:
        company_profile_list.append(new_company_profile)
        out_model.company_profiles = company_profile_list
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error updating company profile")


@router.get("/company_profile_by_id",
            response_model=mappers.UnifiedOutModel,
            response_model_exclude_none=True,
            )
def read_company_profiles_by_id(
        db: Session = Depends(deps.get_db),
        id: str = "",
) -> Any:
    """
    Retrieve company profile by id.
    """
    company_profile = crud.base_users.company_profile.get(db, id=id)
    out_model = mappers.UnifiedOutModel()

    if company_profile is not None:
        out_model.company_profiles = [company_profile]
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error getting company profile by id: %" % id)

    return out_model


@router.get("/company_profile_by_name",
            response_model=mappers.UnifiedOutModel,
            response_model_exclude_none=True,
            )
def read_company_profiles_by_name(
        db: Session = Depends(deps.get_db),
        company_name: str = "",
) -> Any:
    """
    Retrieve company profile by company name.
    """
    company_profile = crud.base_users.company_profile.get_by_name(db, company_name=company_name)
    company_profile_list = list()
    out_model = mappers.UnifiedOutModel()
    if company_profile is not None:
        company_profile_list.append(company_profile)
        out_model.company_profiles = company_profile_list
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error getting company profile by name: %" % company_name)


@router.delete("/", response_model=mappers.UnifiedOutModel, )
def delete_company_profile_details(
        *,
        db: Session = Depends(deps.get_db),
        company_profile_id: str,
) -> Any:
    """
    Delete company profile details.
    """
    out_model = mappers.UnifiedOutModel()
    company_list = list()

    if company_profile_id:
        cp_out = crud.base_users.company_profile.get_by_id(
            db, id=company_profile_id)

        if cp_out:
            deleted_data = crud.base_users.company_profile.remove_by_id(
                db, company_id=company_profile_id)
        else:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail="Company profile details for '%s' not found" % company_profile_id)
    else:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Insufficient request details")

    if deleted_data is not None:
        company_list.append(cp_out)
        out_model.company_profiles = company_list
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error deleting company profile details for '%s' " % company_profile_id)

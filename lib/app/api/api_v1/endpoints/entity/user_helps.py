from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lib.app import crud, models, schemas,mappers
from lib.app.api import deps

from pydantic import parse_obj_as
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from lib.app.auth.firebase_auth import AuthInterceptor
from fastapi import Depends

jwt_bearer = AuthInterceptor()
router = APIRouter()


# not used in the code - we use firebase
@router.get("/login", response_model=str)
def login(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
        claims : dict = Depends(AuthInterceptor.approve)
) -> Any:
    # check login details and return user data
    detail = ''
    phone_number = claims["phone"]

    if phone_number is None or phone_number == '':
        detail = "insufficient-details"
        result = {'state': detail, 'data': ''}
        return JSONResponse(jsonable_encoder(result))

    base_user = crud.user.get_by_phone_number(db=db, phone_number=phone_number)

    if base_user is None:
        detail = "user-not-found"
        result = {'state': detail, 'data': ''}
        return JSONResponse(jsonable_encoder(result))
    elif not base_user:
        detail = "user-not-found"
        result = {'state': detail, 'data': ''}
        return JSONResponse(jsonable_encoder(result))
    else:
        user = crud.base_user.get_by_phone_number(db=db, phone_number=phone_number)
        if user or user is not None:
            detail = "success"
            data = parse_obj_as(schemas.BaseUser, user)
            result = {'state': detail, 'data': data}
            return JSONResponse(jsonable_encoder(result))
        else:
            detail = "user-not-found"
            result = {'state': detail, 'data': ''}
            return JSONResponse(jsonable_encoder(result))


@router.get("/get_global_contacts_list",
            response_model=mappers.UnifiedOutModel,
            response_model_include=["phone_number", "full_name", "email"],
            response_model_exclude_none=True,
            )
def global_contacts_list(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
        Retrieve shared contacts list
    """
    # check login details and return user data
    contacts_list = crud.user.get_global_contacts(db=db)

    # if not contacts_list:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="Global contact list not found",
    #     )
    
    out_model = mappers.UnifiedOutModel()
    out_model.user = contacts_list
    return out_model


@router.put("/update_share_contact/{user_email}", response_model=mappers.UnifiedOutModel)
def update_share_contact(
        *,
        db: Session = Depends(deps.get_db),
        email: str,
        share_contact: bool,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update share contact flag for user.
    """
    user_by_email = crud.user.get_by_email(db, email=email)
    # if not user_by_email:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="The user with this username does not exist in the system",
    #     )
    user_in = schemas.UserUpdate()
    user_in.share_contact = share_contact
    user = crud.user.update(db, db_obj=user_by_email, obj_in=user_in)
    
    out_model = mappers.UnifiedOutModel()
    out_model.user = [user]
    return user


@router.get("/get_category_list",
            response_model=mappers.UnifiedOutModel,
            response_model_include=["category", "id"],
            response_model_exclude_none=True
            )
def get_category_list(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
        Retrieve category list
    """
    # check login details and return user data
    category_list = crud.category.get_multi(db=db)
    out_model = mappers.UnifiedOutModel()
    out_model.category=category_list
    # if not category_list:
    #     raise HTTPException(
    #         status_code=404,
    #         detail="Category list not found",
    #     )

    return out_model

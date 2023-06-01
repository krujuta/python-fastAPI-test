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


@router.get("/",
            response_model=mappers.UnifiedOutModel,
            response_model_exclude_none=True,)
def read_base_users(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    out_model = mappers.UnifiedOutModel()
    base_users = crud.base_users.base_user.get_multi(db, skip=skip, limit=limit)

    if base_users is None:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Users not found")
    else:
        out_model.created_users = base_users
        return out_model


@router.post("/", response_model=mappers.UnifiedOutModel,
             response_model_exclude_none=True)
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: mappers.UnifiedInModel,
        # password: str = None,
) -> Any:
    """
    Create new base user.
    """
    user_in = user_in.created_user

    if user_in is None:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Insufficient request details")

    user = crud.base_users.base_user.get_by_phone_number(
        db, phone_number=user_in.phone_number)

    out_user = crud.base_users.base_user.create(db, obj_in=user_in)

    public_user = schemas.UserCreate(
        phone_number=out_user.phone_number,
        is_active=True,
        full_name=out_user.name,
        email=out_user.email,
        password=""
    )

    # add base_user in public.user table to enable logic functionality
    user = crud.user.create_user_firebase(db, obj_in=public_user)

    # Add user to company users list

    out_model = mappers.UnifiedOutModel()
    if out_user is not None:
        out_model.created_users = [out_user]
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error creating user details")


@router.get("/get_user_details",
            response_model=mappers.UnifiedOutModel,
            response_model_exclude_none=True)
def read_user_by_id(
        db: Session = Depends(deps.get_db),
        user_id: str = "",
        phone_number: str = "",
) -> Any:
    """
    Retrieve users by user id or phone number.
    """
    out_model = mappers.UnifiedOutModel()
    user_list = list()

    param = ""
    if user_id:
        param = user_id
        base_user = crud.base_users.base_user.get_by_id(
            db, user_id=user_id)
    elif phone_number:
        param = phone_number
        base_user = crud.base_users.base_user.get_by_phone_number(
            db, phone_number=phone_number)
    else:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Insufficient request details")

    if base_user is not None:
        user_list.append(base_user)
        out_model.created_users = user_list
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="User details for %s not found" % param)


@router.put("/update", response_model=mappers.UnifiedOutModel)
def update_user_profile(
        *,
        db: Session = Depends(deps.get_db),
        in_model: mappers.UnifiedInModel,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    out_model = mappers.UnifiedOutModel()
    user_list = list()

    if in_model.created_user is not None:
        user_id = in_model.created_user.id
        user = crud.base_users.base_user.get(db, id=user_id)
        if user:
            user_out = crud.base_users.base_user.update(
                db, db_obj=user, obj_in=in_model.created_user)
        else:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND, detail="User for '%s' not found" % user_id)

        if user_out is not None:
            user_list.append(user_out)
            out_model.created_users = user_list
            return out_model
        else:
            raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                  detail="Error updating user details")
    else:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Insufficient request details : request body not found")


@router.delete("/", response_model=mappers.UnifiedOutModel, )
def delete_base_user_details(
        *,
        db: Session = Depends(deps.get_db),
        user_id: str,
) -> Any:
    """
    Delete Base User details.
    """
    out_model = mappers.UnifiedOutModel()
    users_list = list()

    if user_id:
        user_out = crud.base_users.base_user.get_by_id(
            db, user_id=user_id)

        if user_out:
            deleted_data = crud.base_users.base_user.remove_by_id(
                db, user_id=user_id)
        else:
            raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail="User details for '%s' not found" % user_id)
    else:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Insufficient request details")

    if deleted_data is not None:
        users_list.append(user_out)
        out_model.created_users = users_list
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error deleting base user details for '%s' " % user_id)

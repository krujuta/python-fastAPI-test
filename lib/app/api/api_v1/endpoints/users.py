from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas,mappers
from app.api import deps
from app.core.config import settings

from lib.app.error_handling.exceptions import CustomException

router = APIRouter()


@router.get("/", response_model=mappers.UnifiedOutModel)
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    out_model = mappers.UnifiedOutModel()
    if users is not None:
        out_model.user = users
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Users not found")


# @router.post("/", response_model=schemas.User)
# def create_user(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_in: schemas.UserCreate,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Create new user.
#     """
#     user = crud.user.get_by_email(db, email=user_in.email)
#     if user:
#         raise HTTPException(
#             status_code=400,
#             detail="The user with this username already exists in the system.",
#         )
#     user = crud.user.create(db, obj_in=user_in)
#     if settings.EMAILS_ENABLED and user_in.email:
#         send_new_account_email(
#             email_to=user_in.email, username=user_in.email, password=user_in.password
#         )
#     return user


@router.put("/me", response_model=mappers.UnifiedOutModel)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    out_model = mappers.UnifiedOutModel()
    if user is not None:
        out_model.user = [user]
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error Updating user details")


@router.get("/me", response_model=mappers.UnifiedOutModel)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    out_model = mappers.UnifiedOutModel()
    if current_user is not None:
        out_model.user = [current_user]
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="User details not found")


@router.post("/open", response_model=mappers.UnifiedOutModel) # need to check with ui if it is used
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise CustomException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise CustomException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)
    out_model = mappers.UnifiedOutModel()

    out_model.user = [schemas.User]
    return out_model


@router.get("/{user_id}", response_model=mappers.UnifiedOutModel)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise CustomException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    
    out_model = mappers.UnifiedOutModel()
    if user is not None:
        out_model.user = [user]
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="User not found")


@router.get("/service_providers", response_model=mappers.UnifiedOutModel)
def get_service_providers_list(
        current_user: models.User = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get_service_providers(db)
    out_model = mappers.UnifiedOutModel()
    if user is not None:
        out_model.user = [user]
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Service providers not found")


@router.get("/machine_users", response_model=mappers.UnifiedOutModel)
def get_machine_users_list(
        current_user: models.User = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    TM_U_Requested_inbox_DeleteAction
    """
    user = crud.user.get_machine_users(db)
    out_model = mappers.UnifiedOutModel()
    if user is not None:
        out_model.user = [user]
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_404_NOT_FOUND,
                              detail="Machine users not found")


@router.put("/{user_id}", response_model=mappers.UnifiedOutModel)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise CustomException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    out_model = mappers.UnifiedOutModel()
    if user is not None:
        out_model.user = [user]
        return out_model
    else:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              detail="Error updating user details")

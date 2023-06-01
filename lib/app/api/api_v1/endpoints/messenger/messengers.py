from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from lib.app import crud, models, schemas
from lib.app.api import deps
from lib.app.auth.firebase_auth import AuthInterceptor
from fastapi import Depends

jwt_bearer = AuthInterceptor()
router = APIRouter()


@router.get("/", response_model=List[schemas.messenger.OfflineData])
def read_offline_data(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    offline_data = crud.offline_data.get_multi(db, skip=skip, limit=limit)
    return offline_data


@router.get("/get_messages_by_sender_id", response_model=List[schemas.messenger.OfflineData])
def get_messages_by_sender_id(
        db: Session = Depends(deps.get_db),
        sender_id: int = 0,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    offline_data = crud.offline_data.get_by_sender_id(db, sender_id=sender_id)
    return offline_data


@router.get("/get_messages_by_receiver_id", response_model=List[schemas.messenger.OfflineData])
def get_messages_by_receiver_id(
        db: Session = Depends(deps.get_db),
        receiver_id: int = 0,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    offline_data = crud.offline_data.get_by_receiver_id(db, receiver_id=receiver_id)
    return offline_data


@router.post("/", response_model=schemas.messenger.OfflineData)
def create_offline_data(
        *,
        db: Session = Depends(deps.get_db),
        messenger_data: schemas.messenger.OfflineDataCreate,
) -> Any:
    """
    post messenger data.
    """

    data = crud.offline_data.create(db, obj_in=messenger_data)

    # if data is None:
    #     raise HTTPException(
    #         status_code=500,
    #         detail="Error adding the data to backend",
    #     )

    return data


@router.delete("/{id}", response_model=schemas.messenger.OfflineData)
def delete_by_id(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    # delete service detail by id

    data = crud.offline_data.get(db=db, id=id)
    # if not data:
    #     raise HTTPException(status_code=500, detail="Item not found")
    # if not crud.user.is_superuser(current_user) and (data.owner_id != current_user.id):
    #     raise HTTPException(status_code=400, detail="Not enough permissions")
    data = crud.offline_data.remove(db=db, id=id)
    return data

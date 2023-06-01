from typing import Generator

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from lib.app import crud, models
from lib.app.db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# modified as test data - admin [user.id = test:user:1]
def get_current_user(
        db: Session = Depends(get_db),
) -> models.User:
    user = crud.user.get(db, id='test:user:1')
    return user


def get_current_active_user(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

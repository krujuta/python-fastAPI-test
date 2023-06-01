from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from lib.app.crud.base import CRUDBase
from lib.app.models.user import User
from lib.app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_global_contacts(self, db: Session) -> User:
        return db.query(User).filter(User.share_contact).all()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
            phone_number=obj_in.phone_number,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # create without password for test-users - login using phone_number
    def create_user_firebase(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
            phone_number=obj_in.phone_number,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def is_serviceprovider(self, user: User) -> bool:
        return user.is_serviceprovider

    def is_machineuser(self, user: User) -> bool:
        return user.is_machineuser

    # get by phone number
    def get_by_phone_number(self, db: Session, *, phone_number: str) -> Any:
        user = db.query(User).filter(User.phone_number == phone_number).first()

        if not user:
            return None
        return user

    # get service providers list
    def get_service_providers(
            self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return (
            db.query(self.model)
            .filter(User.is_serviceprovider)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get machine users list
    def get_machine_users(
            self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return (
            db.query(self.model)
            .filter(User.is_machineuser)
            .offset(skip)
            .limit(limit)
            .all()
        )


user = CRUDUser(User)

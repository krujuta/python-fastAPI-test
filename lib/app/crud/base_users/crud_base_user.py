from typing import List, Optional, Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from lib.app.crud.base import CRUDBase
from lib.app.models.base_users.base_user import BaseUser
from lib.app.schemas.base_users.base_user import BaseUserCreate, BaseUserUpdate


class CRUDBaseUser(CRUDBase[BaseUser, BaseUserCreate, BaseUserUpdate]):
    def create_with_owner(
            self, db: Session, *, obj_in: BaseUserCreate
    ) -> BaseUser:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create(self, db: Session, *, obj_in: BaseUserCreate) -> BaseUser:
        db_obj = BaseUser(
            name=obj_in.name,
            job_title=obj_in.job_title,
            phone_number=obj_in.phone_number,
            email=obj_in.email,
            is_admin=obj_in.is_admin,
            is_normal_user=obj_in.is_normal_user,
            company_profile_id=obj_in.company_profile_id,
            is_service_provider=obj_in.is_service_provider,
            is_machine_user=obj_in.is_machine_user,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[BaseUser]:
        return (
            db.query(self.model)
            .filter(BaseUser.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get user details by id
    def get_by_id(self, db: Session, *, user_id: str) -> Optional[BaseUser]:
        return db.query(BaseUser).filter(BaseUser.id == user_id).first()

    # get user details by username
    def get_by_email(self, db: Session, *, email: str) -> Optional[BaseUser]:
        return db.query(BaseUser).filter(BaseUser.email == email).first()

    def get_by_phone_number(self, db: Session, *, phone_number: str) -> Optional[BaseUser]:
        user = db.query(BaseUser).filter(BaseUser.phone_number == phone_number).first()
        if user:
            return user
        else:
            return None

    def update(
            self, db: Session, *, db_obj: BaseUser, obj_in: Union[BaseUserUpdate, Dict[str, Any]]
    ) -> BaseUser:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def remove_by_id(self, db: Session, *, user_id: str) -> Any:
        return super().remove_str_id(db, id=user_id)


base_user = CRUDBaseUser(BaseUser)


from typing import List, Optional, Union, List, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from lib.app.crud.base import CRUDBase
from lib.app.models.messenger.offline_data import OfflineData
from lib.app.schemas.messenger.offline_data import OfflineDataCreate, OfflineDataUpdate


class CRUDCompanyProfile(CRUDBase[OfflineData, OfflineDataCreate, OfflineDataUpdate]):
    def create_with_owner(
            self, db: Session, *, obj_in: OfflineDataCreate
    ) -> OfflineData:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[OfflineData]:
        return (
            db.query(self.model)
            .filter(OfflineData.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get user details by username
    # def get_by_email(self, db: Session, *, email: str) -> Optional[OfflineData]:
    #     return db.query(OfflineData).filter(OfflineData.email == email).first()

    def update(
            self, db: Session, *, db_obj: OfflineData, obj_in: Union[OfflineDataUpdate, Dict[str, Any]]
    ) -> OfflineData:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    #  get by sender_id
    def get_by_sender_id(
            self, db: Session, sender_id: int, skip: int = 0, limit: int = 100
    ) -> List[OfflineData]:
        return (
            db.query(self.model)
            .filter(OfflineData.sender_id == sender_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        #  get by sender_id
    def get_by_receiver_id(
            self, db: Session, receiver_id: int, skip: int = 0, limit: int = 100
    ) -> List[OfflineData]:
        return (
            db.query(self.model)
            .filter(OfflineData.receiver_id == receiver_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


offline_data = CRUDCompanyProfile(OfflineData)

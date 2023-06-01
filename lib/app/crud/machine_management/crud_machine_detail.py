from typing import Any, Dict, Optional, Union, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from lib.app.crud.base import CRUDBase
from lib.app.models.machine_management import MachineDetail
from lib.app.schemas.machine_management.machine_detail import MachineDetailCreate, MachineDetailUpdate


class CRUDMachineDetail(CRUDBase[MachineDetail, MachineDetailCreate, MachineDetailUpdate]):

    def create_with_owner(
            self, db: Session, *, obj_in: MachineDetailCreate
    ) -> MachineDetail:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create(
            self, db: Session, *, obj_in: MachineDetailCreate
    ) -> MachineDetail:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[MachineDetail]:
        return (
            db.query(self.model)
            .filter(MachineDetail.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[MachineDetail]:
        return (
            db.query(self.model)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, db: Session, *, machine_id: str) -> Any:
        return db.query(self.model).filter(MachineDetail.id == machine_id).first()

    def remove_by_id(self, db: Session, *, machine_id: str) -> Any:
        return super().remove_str_id(db, id=machine_id)

    def get_by_machine_name(self, db: Session, *, machine_name: str) -> Any:
        return db.query(self.model).filter(MachineDetail.machine == machine_name).first()

    # get by machine type
    def get_multi_by_machine_type(
            self, db: Session, machine_type: str, skip: int = 0, limit: int = 100
    ) -> List[MachineDetail]:
        return (
            db.query(self.model)
            .filter(MachineDetail.machine_type == machine_type)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get by machine manufacturer
    def get_multi_by_machine_manufacturer(
            self, db: Session, machine_manufacturer: str, skip: int = 0, limit: int = 100
    ) -> List[MachineDetail]:
        return (
            db.query(self.model)
            .filter(MachineDetail.machine_oem == machine_manufacturer)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(
            self, db: Session, *, db_obj: MachineDetail, obj_in: Union[MachineDetailUpdate, Dict[str, Any]]
    ) -> MachineDetail:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


machine_detail = CRUDMachineDetail(MachineDetail)

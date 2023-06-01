from typing import List, Union, Dict, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from lib.app.crud.base import CRUDBase
from lib.app.models.my_services import ServiceStatus
from lib.app.schemas.my_services.service_status import ServiceStatusCreate, ServiceStatusUpdate


class CRUDServiceStatus(CRUDBase[ServiceStatus, ServiceStatusCreate, ServiceStatusUpdate]):

    def create_with_owner(
        self, db: Session, *, obj_in: ServiceStatusCreate
    ) -> ServiceStatus:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[ServiceStatus]:
        return (
            db.query(self.model)
            .filter(ServiceStatus.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    #  get by user_id
    def get_multi_by_user_id(
            self, db: Session, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[ServiceStatus]:
        return (
            db.query(self.model)
            .filter(ServiceStatus.processed_by_user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    #  get by service_provider_id
    def get_multi_by_service_provider_request_status(
            self,
            db: Session,
            service_provider_id: str,
            request_status: str,
            skip: int = 0,
            limit: int = 100
    ) -> List[ServiceStatus]:
        return (
            db.query(self.model)
            .filter(ServiceStatus.service_provider_id == service_provider_id)
            .filter(ServiceStatus.status == request_status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # get by user type : service provider / machine user
    def get_multi_by_user_type(
            self, db: Session, service_provider: bool,
            machine_user: bool, skip: int = 0, limit: int = 100
    ) -> List[ServiceStatus]:
        if service_provider:
            return (
                db.query(self.model)
                .filter(ServiceStatus.request_for_serviceprovider == service_provider)
                .offset(skip)
                .limit(limit)
                .all()
            )
        elif machine_user:
            return (
                db.query(self.model)
                .filter(ServiceStatus.request_for_machineuser == machine_user)
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            return (
                db.query(self.model)
                .filter(ServiceStatus.request_for_serviceprovider == service_provider)
                .filter(ServiceStatus.request_for_machineuser == machine_user)
                .offset(skip)
                .limit(limit)
                .all()
            )

    # get by user type: service provider / machine user
    # and request status: pending, requested etc
    def get_multi_by_user_type_and_status(
            self, db: Session, service_provider: bool,
            machine_user: bool, request_status: str, skip: int = 0, limit: int = 100
    ) -> List[ServiceStatus]:
        if service_provider:
            return (
                db.query(self.model)
                .filter(ServiceStatus.request_for_serviceprovider == service_provider)
                .filter(ServiceStatus.status == request_status)
                .offset(skip)
                .limit(limit)
                .all()
            )
        elif machine_user:
            return (
                db.query(self.model)
                .filter(ServiceStatus.request_for_machineuser == machine_user)
                .filter(ServiceStatus.status == request_status)
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            return (
                db.query(self.model)
                .filter(ServiceStatus.request_for_serviceprovider == service_provider)
                .filter(ServiceStatus.request_for_machineuser == machine_user)
                .filter(ServiceStatus.status == request_status)
                .offset(skip)
                .limit(limit)
                .all()
            )

    def update(
            self, db: Session, *, db_obj: ServiceStatus, obj_in: Union[ServiceStatusUpdate, Dict[str, Any]]
    ) -> ServiceStatus:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


service_status = CRUDServiceStatus(ServiceStatus)


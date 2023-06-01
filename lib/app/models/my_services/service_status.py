from sqlalchemy import Column, String, Boolean, Sequence, Integer, ForeignKey
from lib.app.db.base_class import Base
from sqlalchemy.orm import relationship


class ServiceStatus(Base):
    TABLE_ID = Sequence('servicestatus_seq_xxx')
    id = Column(String, primary_key=True, index=True, nullable=False, server_default=TABLE_ID.next_value())
    service_detail_id = Column(String, ForeignKey("servicedetail.id"))
    service_details = relationship("ServiceDetail", foreign_keys="ServiceStatus.service_detail_id")
    status = Column(String, index=True, default='')
    request_for_serviceprovider = Column(Boolean(), default=False)
    request_for_machineuser = Column(Boolean(), default=False)
    processed_by_user_id = Column(Integer, ForeignKey("baseuser.id"))
    processed_by_user = relationship("BaseUser",
                                     foreign_keys='ServiceStatus.processed_by_user_id')
    service_provider_id = Column(Integer, ForeignKey("baseuser.id"))


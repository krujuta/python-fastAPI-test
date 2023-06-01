from lib.app.db.base_class import Base
from sqlalchemy import Column, String, Sequence, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship


class CommentDetail(Base):
    TABLE_ID = Sequence('commentdetail_seq_xxx')
    id = Column(String, primary_key=True, index=True, nullable=False, server_default=TABLE_ID.next_value())
    comment = Column(String, index=True, nullable=False)
    timestamp = Column(TIMESTAMP, index=True, nullable=False)
    created_user_id = Column(String, ForeignKey('baseuser.id'))
    company_profile_id = Column(String, ForeignKey('companyprofile.id'))
    service_detail_id = Column(String, ForeignKey("servicedetail.id"))

    service_status_id = Column(String, ForeignKey("servicestatus.id"))
    service_status = relationship("ServiceStatus", foreign_keys="CommentDetail.service_status_id")

    created_user_profile = relationship("BaseUser", foreign_keys="CommentDetail.created_user_id")

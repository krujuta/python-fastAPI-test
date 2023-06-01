from sqlalchemy import Column, Integer, String, Boolean, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from lib.app.db.base_class import Base


class ServiceDetail(Base):
    TABLE_ID = Sequence('servicedetail_seq_xxx')
    id = Column(String, primary_key=True, index=True, nullable=False, server_default=TABLE_ID.next_value())
    address = Column(String, index=True, default='None')

    note = Column(String, index=True, default='None')
    created_date = Column(String, index=True, default='None')
    created_user_id = Column(String, ForeignKey('user.id'))
    price = Column(Integer, index=True, default=0)
    # control_manufactor_series = controller OEM
    company_profile_id = Column(String, ForeignKey('companyprofile.id'))
    company_profile = relationship("CompanyProfile", foreign_keys="ServiceDetail.company_profile_id")

    category_id = Column(String, ForeignKey('category.id'))
    category = relationship("Category", foreign_keys="ServiceDetail.category_id")

    request_for_serviceprovider = Column(Boolean(), default=False)
    request_for_user = Column(Boolean(), default=False)

from lib.app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, Sequence


class User(Base):
    TABLE_ID = Sequence('user_seq_xxx')
    id = Column(String, primary_key=True, index=True, nullable=False, server_default=TABLE_ID.next_value())
    full_name = Column(String, index=True, default='')
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, default='')
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    share_contact = Column(Boolean(), default=False)
    phone_number = Column(String, index=True, default='')


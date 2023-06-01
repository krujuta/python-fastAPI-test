from sqlalchemy import Column, Sequence, String,Integer

from lib.app.db.base_class import Base


class Category(Base):
    TABLE_ID = Sequence('category_seq_xxx')
    id = Column(String, primary_key=True, index=True, nullable=False, server_default=TABLE_ID.next_value())
    category = Column(String, index=True, default='')
    date = Column(String, index=True, default='')
    controller = Column(String, index=True, default='')
    brand = Column(String, index=True, default='')

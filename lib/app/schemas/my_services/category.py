from pydantic import BaseModel
from typing import Optional


# Shared properties
class CategoryBase(BaseModel):
    category: Optional[str] = ""


# Properties to receive on item creation
class CategoryCreate(CategoryBase):
    category: Optional[str] = ""
    date: Optional[str] = ""
    controller: Optional[str] = ""
    brand: Optional[str] = ""


# Properties to receive on item update
class CategoryUpdate(CategoryBase):
    pass


# Properties shared by models stored in DB
class CategoryInDBBase(CategoryBase):
    # id: Optional[int]
    category: Optional[str] = ""

    class Config:
        orm_mode = True


# Properties to return to client
class Category(CategoryInDBBase):
    id: Optional[str]
    category: Optional[str] = ""
    pass


# Properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass

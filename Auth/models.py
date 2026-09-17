from typing import Optional
from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ItemUpdate(BaseModel):      
    name: str
    description: Optional[str] = None


class ItemPatch(BaseModel):         
    name: Optional[str] = None
    description: Optional[str] = None


class User(BaseModel):
    username: str
    role: str
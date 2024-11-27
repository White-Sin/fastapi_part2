from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AdvertisementBase(BaseModel):
    title: str
    description: str
    price: float


class AdvertisementCreate(AdvertisementBase):
    pass


class AdvertisementUpdate(AdvertisementBase):
    pass


class AdvertisementInDB(AdvertisementBase):
    id: int
    created_at: datetime
    author_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str]


class UserInDB(UserBase):
    id: int
    group: str
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    group: str

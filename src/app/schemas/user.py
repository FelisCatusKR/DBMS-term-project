from __future__ import annotations
from typing import Optional, List
from pydantic import *


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: str
    password: str
    tel: constr(regex="^(0\d{1,2})?-?\d{3,4}-?\d{4}$")
    lon: float
    lat: float


class UserRegister(UserBase):
    hosp_id: Optional[int] = None
    shop_id: Optional[int] = None


class UserUpdate(UserBase):
    password: str
    name: Optional[str] = None
    email: Optional[str] = None
    tel: Optional[constr(regex="^(0\d{1,2})?-?\d{3,4}-?\d{4}$")] = None
    lon: Optional[float] = None
    lat: Optional[float] = None


class User(UserBase):
    id: int
    tel: str
    lon: float
    lat: float
    is_active: bool
    hosp_id: Optional[int]
    shop_id: Optional[int]
    hospital_reservations: List[HospReservation] = []
    shop_reservations: List[ShopReservation] = []

    class Config(BaseConfig):
        orm_mode = True


from app.schemas.reservation import HospReservation, ShopReservation

User.update_forward_refs()

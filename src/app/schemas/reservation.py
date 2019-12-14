from __future__ import annotations
from typing import Optional
from datetime import datetime
from pydantic import *


class HospReservationBase(BaseModel):
    pass


class HospReservationCreate(HospReservationBase):
    user_id: int
    date: datetime


class HospReservation(HospReservationBase):
    id: int
    user_id: Optional[int]
    hosp_id: Optional[int]
    date: datetime

    class Config(BaseConfig):
        orm_mode = True


class ShopReservationBase(BaseModel):
    pass


class ShopReservationCreate(ShopReservationBase):
    user_id: int
    date: datetime
    prescription_id: int


class ShopReservationUpdate(ShopReservationBase):
    is_able_to_prescribe: bool


class ShopReservation(ShopReservationBase):
    id: int
    user_id: Optional[int]
    shop_id: Optional[int]
    date: datetime
    prescription_id: Optional[int]
    prescription: Optional[Prescription]
    is_able_to_prescribe: Optional[bool]

    class Config(BaseConfig):
        orm_mode = True


from app.schemas.prescription import Prescription

ShopReservation.update_forward_refs()

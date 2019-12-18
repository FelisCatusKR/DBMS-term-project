from __future__ import annotations
from datetime import time
from typing import Optional, List
from pydantic import *


class HospitalBase(BaseModel):
    dutyTime1s: Optional[time] = None
    dutyTime1c: Optional[time] = None
    dutyTime2s: Optional[time] = None
    dutyTime2c: Optional[time] = None
    dutyTime3s: Optional[time] = None
    dutyTime3c: Optional[time] = None
    dutyTime4s: Optional[time] = None
    dutyTime4c: Optional[time] = None
    dutyTime5s: Optional[time] = None
    dutyTime5c: Optional[time] = None
    dutyTime6s: Optional[time] = None
    dutyTime6c: Optional[time] = None
    dutyTime7s: Optional[time] = None
    dutyTime7c: Optional[time] = None
    dutyTime8s: Optional[time] = None
    dutyTime8c: Optional[time] = None


class HospitalCreate(HospitalBase):
    name: constr(min_length=1)
    addr: constr(min_length=1)
    tel: constr(regex="^(0\d{1,2})?-?\d{3,4}-?\d{4}$")
    lon: confloat(ge=-180.0, le=180.0)
    lat: confloat(ge=-90.0, le=90.0)
    strCnd: conint(ge=1)
    course_bitmask: conint(ge=1, lt=2 ** 29)


class HospitalUpdate(HospitalBase):
    name: Optional[constr(min_length=1)] = None
    addr: Optional[constr(min_length=1)] = None
    tel: Optional[constr(regex="^(0\d{1,2})?-?\d{3,4}-?\d{4}$")] = None
    strCnd: Optional[conint(ge=1)] = None
    course_bitmask: Optional[conint(ge=1, lt=2 ** 29)]


class Hospital(HospitalBase):
    id: int
    name: str
    addr: str
    tel: str
    lon: float
    lat: float
    strCnd: int
    course_bitmask: int
    doctors: List[User] = []
    reservations: List[HospReservation] = []

    class Config:
        orm_mode = True


from app.schemas.user import User
from app.schemas.reservation import HospReservation

Hospital.update_forward_refs()

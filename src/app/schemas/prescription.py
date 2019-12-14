from __future__ import annotations
from typing import Optional, List
from pydantic import *
from datetime import datetime


class PrescriptionBase(BaseModel):
    pass


class PrescriptionCreate(PrescriptionBase):
    hospital_reservation_id: conint(ge=1)
    prescribed_date: datetime


class PrescriptionUpdate(PrescriptionBase):
    filled_shop_id: int
    filled_date: datetime
    filled_detail: str


class Prescription(PrescriptionBase):
    id: int
    hospital_reservation_id: Optional[int]
    hospital_reservation: Optional[HospReservation]
    filled_shop_id: Optional[int]
    filled_date: Optional[datetime]
    filled_detail: Optional[str]
    filled_drugs: List[PrescribedDrug] = []

    class Config(BaseConfig):
        orm_mode = True


from app.schemas.reservation import HospReservation
from app.schemas.drug import PrescribedDrug

Prescription.update_forward_refs()

from __future__ import annotations
from typing import Optional, List
from pydantic import *
from datetime import datetime


class PrescribedDrugBase(BaseModel):
    pass


class PrescribedDrugCreate(PrescribedDrugBase):
    drug_id: conint(ge=1)
    drug_amount_per_dose: conint(ge=1)
    drug_doses_per_day: conint(ge=1)
    drug_total_days: conint(ge=1)


class PrescribedDrug(PrescribedDrugBase):
    id: int
    drug_id: Optional[int]
    drug: Optional[Drug]
    drug_amount_per_dose: int
    drug_doses_per_day: int
    drug_total_days: int
    prescription_id: Optional[int]

    class Config(BaseConfig):
        orm_mode = True


class PrescriptionBase(BaseModel):
    pass


class PrescriptionCreate(PrescriptionBase):
    hospital_reservation_id: conint(ge=1)
    prescribed_date: datetime
    prescribed_drugs: List[PrescribedDrugCreate]


class PrescriptionUpdate(PrescriptionBase):
    filled_shop_id: int
    filled_date: datetime
    filled_detail: str


class Prescription(PrescriptionBase):
    id: int
    hospital_reservation_id: Optional[int]
    hospital_reservation: Optional[HospReservation]
    prescribed_date: datetime
    prescribed_drugs: List[Optional[PrescribedDrug]]
    filled_shop_id: Optional[int]
    filled_date: Optional[datetime]
    filled_detail: Optional[str]

    class Config(BaseConfig):
        orm_mode = True


from app.schemas.drug import Drug
from app.schemas.reservation import HospReservation

PrescribedDrug.update_forward_refs()
PrescriptionCreate.update_forward_refs()
Prescription.update_forward_refs()

from __future__ import annotations
from typing import Optional, List
from pydantic import *


class DrugBase(BaseModel):
    name: Optional[str]
    unit: Optional[str]


class DrugCreate(DrugBase):
    name: str


class DrugUpdate(DrugBase):
    pass


class Drug(DrugBase):
    id: int
    name: str
    prescribed_list: List[PrescribedDrug] = []

    class Config(BaseConfig):
        orm_mode = True


class PrescribedDrugBase(BaseModel):
    prescription_id: conint(ge=1)
    drug_amount_per_taking: conint(ge=1)
    drug_doses_per_day: conint(ge=1)
    drug_total_days: conint(ge=1)


class PrescribedDrugCreate(PrescribedDrugBase):
    pass


class PrescribedDrugUpdate(PrescribedDrugBase):
    prescription_id: Optional[conint(ge=1)]
    drug_amount_per_taking: Optional[conint(ge=1)]
    drug_doses_per_day: Optional[conint(ge=1)]
    drug_total_days: Optional[conint(ge=1)]


class PrescribedDrug(PrescribedDrugBase):
    id: int
    drug_id: Optional[int]
    drug: Optional[Drug]

    class Config(BaseConfig):
        orm_mode = True


Drug.update_forward_refs()
PrescribedDrug.update_forward_refs()

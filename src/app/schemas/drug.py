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

    class Config(BaseConfig):
        orm_mode = True

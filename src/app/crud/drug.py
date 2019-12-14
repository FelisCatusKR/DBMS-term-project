from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import *
from fastapi.encoders import jsonable_encoder

from app.models.drug import Drug
from app.schemas.drug import DrugCreate, DrugUpdate


def read(db: Session, drug_id: int) -> Optional[Drug]:
    return db.query(Drug).filter(Drug.id == drug_id).first()


def read_by_name(db: Session, name: str) -> List[Optional[Drug]]:
    return db.query(Drug).filter(Drug.name.ilike(f"%{name}%")).all()


def read_multi(db: Session, *, skip=0, limit=100) -> List[Optional[Drug]]:
    return db.query(Drug).offset(skip).limit(limit).all()


def create(db: Session, drug: DrugCreate) -> Drug:
    db_drug = Drug(name=drug.name, unit=drug.unit)
    db.add(db_drug)
    db.commit()
    db.refresh(db_drug)
    return db_drug


def update(db: Session, *, drug: Drug, drug_in: DrugUpdate) -> Drug:
    original_data = jsonable_encoder(drug)
    update_data = drug_in.dict(skip_defaults=True)
    for field in original_data:
        if field in update_data:
            setattr(drug, field, update_data[field])
    db.add(drug)
    db.commit()
    db.refresh(drug)
    return drug

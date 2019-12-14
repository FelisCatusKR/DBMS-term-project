from typing import List, Optional
from pydantic import *
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionUpdate,
)
from app.models.prescription import Prescription


def read_prescriptions(db: Session, *, skip: int, limit: int,) -> List[Prescription]:
    return db.query(Prescription).offset(skip).limit(limit).all()


def read(db: Session, *, prescription_id: int) -> Optional[Prescription]:
    return db.query(Prescription).filter(Prescription.id == prescription_id).first()


def read_by_hospital_reservation_id(
    db: Session, *, hospital_reservation_id: int
) -> Optional[Prescription]:
    return (
        db.query(Prescription)
        .filter(Prescription.hospital_reservation_id == hospital_reservation_id)
        .first()
    )


def create(db: Session, *, pres_in: PrescriptionCreate) -> Prescription:
    db_prescription = Prescription(
        hospital_reservation_id=pres_in.hospital_reservation_id,
        prescribed_date=pres_in.prescribed_date,
    )
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription


def update(
    db: Session, *, pres: Prescription, pres_in: PrescriptionUpdate
) -> Prescription:
    prescription_data = jsonable_encoder(pres)
    update_data = pres_in.dict(skip_defaults=True)
    for field in prescription_data:
        if field in update_data:
            setattr(pres, field, update_data[field])
    db.add(pres)
    db.commit()
    db.refresh(pres)
    return pres

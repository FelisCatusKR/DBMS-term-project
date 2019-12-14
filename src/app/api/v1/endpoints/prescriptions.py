from pydantic import *
from typing import List

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.crud import prescription
from app.schemas.prescription import (
    Prescription,
    PrescriptionCreate,
    PrescriptionUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[Prescription])
def read_prescriptions(
    db: Session = Depends(get_db), *, skip: int = 0, limit: conint(le=100) = 100,
):
    prescriptions = prescription.read_prescriptions(db, skip=skip, limit=limit)
    return prescriptions


@router.post("/", response_model=Prescription)
def create(
    db: Session = Depends(get_db), *, pres: PrescriptionCreate,
):
    if (
        prescription.read_by_hospital_reservation_id(
            db, hospital_reservation_id=PrescriptionCreate.hospital_reservation_id
        )
        is not None
    ):
        raise HTTPException(
            status_code=400,
            detail="Prescription for the hospital reservation ID already registered",
        )
    db_pres = prescription.create(db, pres_in=pres)
    return db_pres


@router.get("/{prescription_id}", response_model=Prescription)
def read(
    db: Session = Depends(get_db),
    *,
    prescription_id: int = Path(..., title="The ID of the prescription to read", ge=1),
):
    drg = prescription.read(db, prescription_id=prescription_id)
    if drg is None:
        raise HTTPException(
            status_code=404, detail="Prescription not found",
        )
    return drg


@router.put("/{prescription_id}", response_model=Prescription)
def update(
    db: Session = Depends(get_db),
    *,
    prescription_id: int = Path(..., title="The ID of the prescription to read", ge=1),
    pres: PrescriptionUpdate,
):

    drg = prescription.read(db, prescription_id=prescription_id)
    if drg is None:
        raise HTTPException(
            status_code=404, detail="Prescription not found",
        )
    drg = prescription.update(db, pres=drg, pres_in=pres)
    return drg

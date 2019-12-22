from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Body, HTTPException
from sqlalchemy.orm import Session
from pydantic import *

from app.api.utils.db import get_db
from app.crud import prescription, reservation
from app.schemas.prescription import (
    Prescription,
    PrescriptionCreate,
    PrescriptionUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[Prescription])
def read_prescriptions(
    hospital_id: Optional[int] = None,
    skip: Optional[int] = 0,
    limit: Optional[conint(le=100)] = 100,
    db: Session = Depends(get_db),
):
    prescriptions = prescription.read_prescriptions(db, hospital_id=hospital_id, skip=skip, limit=limit)
    return prescriptions


@router.post("/", response_model=Prescription)
def create(pres: PrescriptionCreate, db: Session = Depends(get_db)):
    if reservation.read_hosp(db, reservation_id=pres.hospital_reservation_id) is None:
        raise HTTPException(
            status_code=400,
            detail="The submitted hospital reservation ID does not exist",
        )
    if (
        prescription.read_by_hospital_reservation_id(
            db, hospital_reservation_id=pres.hospital_reservation_id
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
    prescription_id: int = Path(..., title="The ID of the prescription to read", ge=1),
    db: Session = Depends(get_db),
):
    drg = prescription.read(db, prescription_id=prescription_id)
    if drg is None:
        raise HTTPException(
            status_code=404, detail="Prescription not found",
        )
    return drg


@router.put("/{prescription_id}", response_model=Prescription)
def update(
    prescription_id: int = Path(..., title="The ID of the prescription to read", ge=1),
    reservation_id: int = Body(
        ..., title="The ID of the shop reservation for validation", ge=1
    ),
    pres_in: PrescriptionUpdate = Body(...),
    db: Session = Depends(get_db),
):
    pres = prescription.read(db, prescription_id=prescription_id)
    if pres is None:
        raise HTTPException(
            status_code=404, detail="Prescription not found",
        )
    if (
        reservation.read_shop(
            db, shop_id=pres_in.filled_shop_id, reservation_id=reservation_id
        )
        is None
    ):
        raise HTTPException(
            status_code=400, detail="Prescription is not suitable for submitted store",
        )
    drg = prescription.update(db, pres=pres, pres_in=pres_in)
    return drg

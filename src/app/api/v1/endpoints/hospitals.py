from pydantic import *
from typing import List, Optional

from fastapi import Depends, APIRouter, Path, HTTPException
from app.database import Session
from app.crud import hospital, reservation
from app.schemas.hospital import Hospital, HospitalCreate, HospitalUpdate
from app.schemas.reservation import (
    HospReservation,
    HospReservationCreate,
)
from app.api.utils.db import get_db

router = APIRouter()


@router.get("/", response_model=List[Hospital])
def read_hospitals(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = 0,
    limit: conint(le=100) = 100,
    lat: confloat(ge=-90.0, le=90.0) = 37.5585146,
    lon: confloat(ge=-180.0, le=180.0) = 127.0331892,
    radius: conint(le=5000) = 5000,
):
    hospitals = hospital.read_by_distance(
        db, q=q, lat=lat, lon=lon, radius=radius, skip=skip, limit=limit
    )
    return hospitals


@router.post("/", response_model=Hospital)
def create(db: Session = Depends(get_db), *, hosp_in: HospitalCreate):
    hosp = hospital.create(db, hospital_in=hosp_in)
    return hosp


@router.get("/{hospital_id}", response_model=Hospital)
def read(
    db: Session = Depends(get_db),
    hospital_id: int = Path(..., title="The ID of the hospital to read", ge=1),
):
    hosp = hospital.read(db, hospital_id=hospital_id)
    if not hosp:
        raise HTTPException(
            status_code=404, detail="Hospital not found",
        )
    return hosp


@router.put("/{hospital_id}", response_model=Hospital)
def update(
    db: Session = Depends(get_db),
    *,
    hospital_id: int = Path(..., title="The ID of the hospital to update", ge=1),
    hospital_in: HospitalUpdate,
):
    hosp = hospital.read(db, hospital_id=hospital_id)
    if not hosp:
        raise HTTPException(
            status_code=404, detail="Hospital not found",
        )
    hosp = hospital.update(db, hospital=hosp, hospital_in=hospital_in)
    return hosp


@router.get("/{hospital_id}/reservations", response_model=List[HospReservation])
def read_reservation_list(
    db: Session = Depends(get_db),
    hospital_id: int = Path(..., title="The ID of the hospital to read", ge=1),
    skip: Optional[int] = 0,
    limit: Optional[conint(le=100)] = 100,
):
    hosp = hospital.read(db, hospital_id=hospital_id)
    if not hosp:
        raise HTTPException(
            status_code=404, detail="Hospital not found",
        )
    reservations = reservation.read_multi_hosp(
        db, hospital_id=hospital_id, skip=skip, limit=limit
    )
    return reservations


@router.post("/{hospital_id}/reservations", response_model=HospReservation)
def create_reservation(
    db: Session = Depends(get_db),
    *,
    hospital_id: int = Path(..., title="The ID of the hospital to read", ge=1),
    rsrv_in: HospReservationCreate,
):
    hosp = hospital.read(db, hospital_id=hospital_id)
    if not hosp:
        raise HTTPException(
            status_code=404, detail="Hospital not found",
        )
    hosp_reservation = reservation.create_hosp(
        db, hospital_id=hospital_id, rsrv_in=rsrv_in
    )
    return hosp_reservation


@router.get(
    "/{hospital_id}/reservations/{reservation_id}", response_model=HospReservation
)
def read_reservation(
    db: Session = Depends(get_db),
    hospital_id: int = Path(..., title="The ID of the hospital to read", ge=1),
    reservation_id: int = Path(..., title="The ID of the reservation to read", ge=1),
):
    hosp = hospital.read(db, hospital_id=hospital_id)
    if not hosp:
        raise HTTPException(
            status_code=404, detail="Hospital not found",
        )
    hosp_reservation = reservation.read_hosp(
        db, hospital_id=hospital_id, reservation_id=reservation_id
    )
    if not hosp_reservation:
        raise HTTPException(
            status_code=404, detail="Reservation not found",
        )
    return hosp_reservation


@router.delete(
    "/{hospital_id}/reservations/{reservation_id}",
    response_model=Optional[HospReservation],
)
def delete_reservation(
    db: Session = Depends(get_db),
    *,
    hospital_id: int = Path(..., title="The ID of the hospital to read", ge=1),
    reservation_id: int = Path(..., title="The ID of the reservation to read", ge=1),
):
    hsp = hospital.read(db, hospital_id=hospital_id)
    if not hsp:
        raise HTTPException(
            status_code=404, detail="Hospital not found",
        )
    hosp_reservation = reservation.read_hosp(
        db, hospital_id=hospital_id, reservation_id=reservation_id
    )
    if not hosp_reservation:
        raise HTTPException(
            status_code=404, detail="Reservation not found",
        )
    hosp_reservation = reservation.delete_hosp(db, rsrv=hosp_reservation)
    return hosp_reservation

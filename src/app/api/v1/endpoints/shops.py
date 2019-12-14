from pydantic import *
from typing import List, Optional

from fastapi import Depends, APIRouter, HTTPException, Path

from app.database import Session
from app.crud import shop, reservation, prescription
from app.schemas.shop import Shop, ShopCreate, ShopUpdate
from app.schemas.reservation import (
    ShopReservation,
    ShopReservationCreate,
    ShopReservationUpdate,
)
from app.api.utils.db import get_db

router = APIRouter()


@router.get("/", response_model=List[Shop])
def read_shops(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = 0,
    limit: conint(le=100) = 100,
    lat: confloat(ge=-90.0, le=90.0) = 37.5585146,
    lon: confloat(ge=-180.0, le=180.0) = 127.0331892,
    radius: conint(le=5000) = 5000,
):
    shops = shop.read_by_distance(
        db, q=q, lat=lat, lon=lon, radius=radius, skip=skip, limit=limit
    )
    return shops


@router.post("/", response_model=Shop)
def create(db: Session = Depends(get_db), *, shop_in: ShopCreate):
    shp = shop.create(db, shop_in=shop_in)
    return shp


@router.get("/{shop_id}", response_model=Shop)
def read(
    db: Session = Depends(get_db),
    shop_id: int = Path(..., title="The ID of the shop to read", ge=1),
):
    shp = shop.read(db, shop_id=shop_id)
    if not shp:
        raise HTTPException(
            status_code=404, detail="Shop not found",
        )
    return shp


@router.put("/{shop_id}", response_model=Shop)
def update(
    db: Session = Depends(get_db),
    *,
    shop_id: int = Path(..., title="The ID of the shop to update", ge=1),
    shop_in: ShopUpdate,
):
    shp = shop.read(db, shop_id=shop_id)
    if not shp:
        raise HTTPException(
            status_code=404, detail="Shop not found",
        )
    shp = shop.update(db, shop=shp, shop_in=shop_in)
    return shp


@router.get("/{shop_id}/reservations", response_model=List[ShopReservation])
def read_reservation_list(
    db: Session = Depends(get_db),
    shop_id: int = Path(..., title="The ID of the shop to read", ge=1),
    skip: Optional[int] = 0,
    limit: Optional[conint(le=100)] = 100,
):
    shp = shop.read(db, shop_id=shop_id)
    if not shp:
        raise HTTPException(
            status_code=404, detail="Shop not found",
        )
    reservations = reservation.read_multi_shop(
        db, shop_id=shop_id, skip=skip, limit=limit
    )
    return reservations


@router.post("/{shop_id}/reservations", response_model=ShopReservation)
def create_reservation(
    db: Session = Depends(get_db),
    *,
    shop_id: int = Path(..., title="The ID of the shop to read", ge=1),
    rsrv_in: ShopReservationCreate,
):
    shp = shop.read(db, shop_id=shop_id)
    if not shp:
        raise HTTPException(
            status_code=404, detail="Shop not found",
        )
    pres = prescription.read(db, prescription_id=rsrv_in.prescription_id)
    if pres.filled_shop_id is not None:
        raise HTTPException(
            status_code=400,
            detail="The submitted prescription is already filled from another store",
        )
    hosp_rsrv = reservation.read_hosp(db, reservation_id=pres.hospital_reservation_id)
    if rsrv_in.user_id is not hosp_rsrv.user_id:
        raise HTTPException(
            status_code=400,
            detail="The submitted user ID is different with the prescription's one",
        )
    shop_reservation = reservation.create_shop(db, shop_id=shop_id, rsrv_in=rsrv_in)
    return shop_reservation


@router.get("/{shop_id}/reservations/{reservation_id}", response_model=ShopReservation)
def read_reservation(
    db: Session = Depends(get_db),
    shop_id: int = Path(..., title="The ID of the shop to read", ge=1),
    reservation_id: int = Path(..., title="The ID of the reservation to read", ge=1),
):
    shp = shop.read(db, shop_id=shop_id)
    if not shp:
        raise HTTPException(
            status_code=404, detail="Shop not found",
        )
    shop_reservation = reservation.read_shop(
        db, shop_id=shop_id, reservation_id=reservation_id
    )
    if not shop_reservation:
        raise HTTPException(
            status_code=404, detail="Reservation not found",
        )
    return shop_reservation


@router.put("/{shop_id}/reservations/{reservation_id}", response_model=ShopReservation)
def update_reservation(
    db: Session = Depends(get_db),
    *,
    shop_id: int = Path(..., title="The ID of the shop to read", ge=1),
    reservation_id: int = Path(..., title="The ID of the reservation to read", ge=1),
    rsrv_in: ShopReservationUpdate,
):
    shp = shop.read(db, shop_id=shop_id)
    if not shp:
        raise HTTPException(
            status_code=404, detail="Shop not found",
        )
    shop_reservation = reservation.read_shop(
        db, shop_id=shop_id, reservation_id=reservation_id
    )
    if not shop_reservation:
        raise HTTPException(
            status_code=404, detail="Reservation not found",
        )
    shop_reservation = reservation.update_shop(
        db, rsrv=shop_reservation, rsrv_in=rsrv_in
    )
    return shop_reservation

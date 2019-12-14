from typing import List, Optional
from pydantic import *
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.schemas.reservation import (
    HospReservationCreate,
    ShopReservationCreate,
    ShopReservationUpdate,
)
from app.models.reservation import HospReservation, ShopReservation


def read_multi_hosp(
    db: Session, hospital_id: int, skip: int, limit: int
) -> List[HospReservation]:
    return (
        db.query(HospReservation)
        .filter(HospReservation.hosp_id == hospital_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def read_hosp(
    db: Session,
    hospital_id: Optional[int] = None,
    reservation_id: Optional[int] = None,
) -> Optional[HospReservation]:
    if hospital_id is not None and reservation_id is not None:
        return (
            db.query(HospReservation)
            .filter(HospReservation.hosp_id == hospital_id)
            .filter(HospReservation.id == reservation_id)
            .first()
        )
    elif hospital_id is not None:
        return (
            db.query(HospReservation)
            .filter(HospReservation.hosp_id == hospital_id)
            .first()
        )
    elif reservation_id is not None:
        return (
            db.query(HospReservation)
            .filter(HospReservation.id == reservation_id)
            .first()
        )
    else:
        return db.query(HospReservation).first()


def create_hosp(
    db: Session, hospital_id: int, rsrv_in: HospReservationCreate
) -> HospReservation:
    db_reservation = HospReservation(
        user_id=rsrv_in.user_id, hosp_id=hospital_id, date=rsrv_in.date
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def delete_hosp(db: Session, rsrv: HospReservation) -> Optional[HospReservation]:
    rsrv_id = rsrv.id
    db.delete(rsrv)
    db.commit()
    return db.query(HospReservation).filter(HospReservation.id == rsrv_id).first()


def read_multi_shop(
    db: Session, shop_id: int, skip: int, limit: int,
) -> List[ShopReservation]:
    return (
        db.query(ShopReservation)
        .filter(ShopReservation.shop_id == shop_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def read_shop(
    db: Session, shop_id: int, reservation_id: int
) -> Optional[ShopReservation]:
    return (
        db.query(ShopReservation)
        .filter(ShopReservation.shop_id == shop_id)
        .filter(ShopReservation.id == reservation_id)
        .first()
    )


def create_shop(
    db: Session, shop_id: int, rsrv_in: ShopReservationCreate
) -> ShopReservation:
    db_reservation = ShopReservation(
        user_id=rsrv_in.user_id,
        shop_id=shop_id,
        date=rsrv_in.date,
        prescription_id=rsrv_in.prescription_id,
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def update_shop(
    db: Session, rsrv: ShopReservation, rsrv_in: ShopReservationUpdate
) -> ShopReservation:
    reservation_data = jsonable_encoder(rsrv)
    update_data = rsrv_in.dict(skip_defaults=True)
    for field in reservation_data:
        if field in update_data:
            setattr(rsrv, field, update_data[field])
    db.add(rsrv)
    db.commit()
    db.refresh(rsrv)
    return rsrv

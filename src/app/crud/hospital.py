from typing import List, Optional
from sqlalchemy.orm import Session
from geoalchemy2 import *
from fastapi.encoders import jsonable_encoder
from app.schemas.hospital import HospitalCreate, HospitalUpdate
from app.models.hospital import Hospital


def read(db: Session, *, hospital_id: int) -> Optional[Hospital]:
    return db.query(Hospital).filter(Hospital.id == hospital_id).first()


def read_by_distance(
    db: Session,
    *,
    q: Optional[str],
    lon: float,
    lat: float,
    radius: int,
    skip: int,
    limit: int,
) -> List[Optional[Hospital]]:
    point = f"POINT({lon} {lat})"
    if q is None:
        return (
            db.query(Hospital)
            .filter(func.ST_Distance_Sphere(Hospital.geom, point) < radius)
            .order_by(func.ST_Distance_Sphere(Hospital.geom, point))
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        return (
            db.query(Hospital)
            .filter(Hospital.name.like(f"%{q}%"))
            .filter(func.ST_Distance_Sphere(Hospital.geom, point) < radius)
            .order_by(func.ST_Distance_Sphere(Hospital.geom, point))
            .offset(skip)
            .limit(limit)
            .all()
        )


def create(db: Session, *, hospital_in: HospitalCreate) -> Hospital:
    geom = f"POINT({hospital_in.lon} {hospital_in.lat})"
    db_hospital = Hospital(
        name=hospital_in.name,
        addr=hospital_in.addr,
        tel=hospital_in.tel,
        lon=hospital_in.lon,
        lat=hospital_in.lat,
        geom=geom,
        strCnd=hospital_in.strCnd,
        course_bitmask=hospital_in.course_bitmask,
        dutyTime1s=hospital_in.dutyTime1s,
        dutyTime1c=hospital_in.dutyTime1c,
        dutyTime2s=hospital_in.dutyTime2s,
        dutyTime2c=hospital_in.dutyTime2c,
        dutyTime3s=hospital_in.dutyTime3s,
        dutyTime3c=hospital_in.dutyTime3c,
        dutyTime4s=hospital_in.dutyTime4s,
        dutyTime4c=hospital_in.dutyTime4c,
        dutyTime5s=hospital_in.dutyTime5s,
        dutyTime5c=hospital_in.dutyTime5c,
        dutyTime6s=hospital_in.dutyTime6s,
        dutyTime6c=hospital_in.dutyTime6c,
        dutyTime7s=hospital_in.dutyTime7s,
        dutyTime7c=hospital_in.dutyTime7c,
        dutyTime8s=hospital_in.dutyTime8s,
        dutyTime8c=hospital_in.dutyTime8c,
    )
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital


def update(db: Session, *, hospital: Hospital, hospital_in: HospitalUpdate) -> Hospital:
    hospital_data = jsonable_encoder(hospital)
    update_data = hospital_in.dict(skip_defaults=True)
    for field in hospital_data:
        if field in update_data:
            setattr(hospital, field, update_data[field])
    db.add(hospital)
    db.commit()
    db.refresh(hospital)
    return hospital

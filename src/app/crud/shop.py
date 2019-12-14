from typing import List, Optional
from sqlalchemy.orm import Session
from geoalchemy2 import *
from fastapi.encoders import jsonable_encoder
from app.schemas.shop import ShopCreate, ShopUpdate
from app.models.shop import Shop


def read(db: Session, shop_id: int) -> Optional[Shop]:
    return db.query(Shop).filter(Shop.id == shop_id).first()


def read_by_distance(
    db: Session,
    q: Optional[str],
    lon: float,
    lat: float,
    radius: int,
    skip: int,
    limit: int,
) -> List[Optional[Shop]]:
    point = f"POINT({lon} {lat})"
    if q is None:
        return (
            db.query(Shop)
            .filter(func.ST_Distance_Sphere(Shop.geom, point) < radius)
            .order_by(func.ST_Distance_Sphere(Shop.geom, point))
            .offset(skip)
            .limit(limit)
            .all()
        )
    else:
        return (
            db.query(Shop)
            .filter(Shop.name.like(f"%{q}%"))
            .filter(func.ST_Distance_Sphere(Shop.geom, point) < radius)
            .order_by(func.ST_Distance_Sphere(Shop.geom, point))
            .offset(skip)
            .limit(limit)
            .all()
        )


def create(db: Session, shop_in: ShopCreate) -> Shop:
    geom = f"POINT({shop_in.lon} {shop_in.lat})"
    db_shop = Shop(
        name=shop_in.name,
        addr=shop_in.addr,
        tel=shop_in.tel,
        lon=shop_in.lon,
        lat=shop_in.lat,
        geom=geom,
        is_pharmacy=shop_in.is_pharmacy,
        dutyTime1s=shop_in.dutyTime1s,
        dutyTime1c=shop_in.dutyTime1c,
        dutyTime2s=shop_in.dutyTime2s,
        dutyTime2c=shop_in.dutyTime2c,
        dutyTime3s=shop_in.dutyTime3s,
        dutyTime3c=shop_in.dutyTime3c,
        dutyTime4s=shop_in.dutyTime4s,
        dutyTime4c=shop_in.dutyTime4c,
        dutyTime5s=shop_in.dutyTime5s,
        dutyTime5c=shop_in.dutyTime5c,
        dutyTime6s=shop_in.dutyTime6s,
        dutyTime6c=shop_in.dutyTime6c,
        dutyTime7s=shop_in.dutyTime7s,
        dutyTime7c=shop_in.dutyTime7c,
        dutyTime8s=shop_in.dutyTime8s,
        dutyTime8c=shop_in.dutyTime8c,
    )
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop


def update(db: Session, shop: Shop, shop_in: ShopUpdate) -> Shop:
    shop_data = jsonable_encoder(shop)
    update_data = shop_in.dict(skip_defaults=True)
    for field in shop_data:
        if field in update_data:
            setattr(shop, field, update_data[field])
    db.add(shop)
    db.commit()
    db.refresh(shop)
    return shop

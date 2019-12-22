from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.favorite import FavoriteHospital, FavoriteShop


def read_hospital(
    db: Session, user_id: int, hospital_id: int
) -> Optional[FavoriteHospital]:
    return (
        db.query(FavoriteHospital)
        .filter(FavoriteHospital.user_id == user_id)
        .filter(FavoriteHospital.hospital_id == hospital_id)
        .first()
    )


def read_hospital_multi(db: Session, user_id: int) -> List[Optional[FavoriteHospital]]:
    return db.query(FavoriteHospital).filter(FavoriteHospital.user_id == user_id).all()


def read_shop(db: Session, user_id: int, shop_id: int) -> Optional[FavoriteShop]:
    return (
        db.query(FavoriteShop)
        .filter(FavoriteShop.user_id == user_id)
        .filter(FavoriteShop.shop_id == shop_id)
        .first()
    )


def read_shop_multi(db: Session, user_id: int) -> List[Optional[FavoriteShop]]:
    return db.query(FavoriteShop).filter(FavoriteShop.user_id == user_id).all()


def create_hospital(db: Session, user_id: int, hospital_id: int) -> FavoriteHospital:
    db_favorite = FavoriteHospital(user_id=user_id, hospital_id=hospital_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite


def create_shop(db: Session, user_id: int, shop_id: int) -> FavoriteShop:
    db_favorite = FavoriteShop(user_id=user_id, shop_id=shop_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite


def delete_hospital(db: Session, fav: FavoriteHospital) -> Optional[FavoriteHospital]:
    db.delete(fav)
    db.commit()
    return (
        db.query(FavoriteHospital)
        .filter(FavoriteHospital.user_id == fav.user_id)
        .filter(FavoriteHospital.hospital_id == fav.hospital_id)
        .first()
    )


def delete_shop(db: Session, fav: FavoriteShop) -> Optional[FavoriteShop]:
    db.delete(fav)
    db.commit()
    return (
        db.query(FavoriteShop)
        .filter(FavoriteShop.user_id == fav.user_id)
        .filter(FavoriteShop.shop_id == fav.shop_id)
        .first()
    )

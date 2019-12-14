from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi.encoders import jsonable_encoder

from app.models.user import User
from app.schemas.user import UserCreate, UserRegister, UserUpdate


def read(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def read_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def read_by_tel(db: Session, tel: str) -> Optional[User]:
    return db.query(User).filter(User.tel == tel).first()


def authenticate(db_session: Session, *, email: str, password: str) -> Optional[User]:
    user = read_by_email(db_session, email=email)
    if not user:
        return None
    if user.password is not password:
        return None
    return user


def is_hosp_owner(user: User, hosp_id: int) -> bool:
    return user.hosp_id == hosp_id


def is_shop_owner(user: User, shop_id: int) -> bool:
    return user.shop_id == shop_id


def read_multi(db_session: Session, *, skip=0, limit=100) -> List[Optional[User]]:
    return db_session.query(User).offset(skip).limit(limit).all()


def create(db: Session, *, user: UserCreate) -> User:
    geom = f"POINT({user.lon} {user.lat})"
    db_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        tel=user.tel,
        lon=user.lon,
        lat=user.lat,
        geom=geom,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def register(db: Session, *, user: User, user_in: UserRegister) -> User:
    original_data = jsonable_encoder(user)
    update_data = user_in.dict(skip_defaults=True)
    for field in original_data:
        if field in update_data:
            setattr(user, field, update_data[field])
    setattr(user, "is_active", True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update(db: Session, *, user: User, user_in: UserUpdate) -> User:
    original_data = jsonable_encoder(user)
    update_data = user_in.dict(skip_defaults=True)
    for field in original_data:
        if field in update_data:
            setattr(user, field, update_data[field])
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

from pydantic import *
from typing import List, Optional

from fastapi import APIRouter, Depends, Security, Path, HTTPException
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.security import get_current_user
from app.crud import user, favorite, hospital, shop
from app.models.user import User as DBUser
from app.schemas.user import User, UserCreate, UserRegister, UserUpdate
from app.schemas.favorite import FavoriteHospital, FavoriteShop

router = APIRouter()


@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(get_db), skip: int = 0, limit: conint(le=100) = 100,
):
    users = user.read_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=User)
def create(db: Session = Depends(get_db), *, user_in: UserCreate):
    usr = user.create(db, user=user_in)
    return usr


@router.get("/me", response_model=User)
def read_user_me(
    db: Session = Depends(get_db), current_user: DBUser = Security(get_current_user),
):
    """
    Get current user.
    """
    return current_user


@router.get("/{user_id}", response_model=User)
def read(
    db: Session = Depends(get_db),
    user_id: int = Path(..., title="The ID of the user to read", ge=1),
):
    usr = user.read(db, user_id=user_id)
    if not usr:
        raise HTTPException(
            status_code=404, detail="User not found",
        )
    return usr


@router.patch("/{user_id}", response_model=User)
def register(
    db: Session = Depends(get_db),
    *,
    user_id: int = Path(..., title="The ID of the user to register", ge=1),
    user_in: UserRegister,
):
    usr = user.read(db, user_id=user_id)
    if not usr:
        raise HTTPException(
            status_code=404, detail="User not found",
        )
    usr = user.register(db, user=usr, user_in=user_in)
    return usr


@router.put("/{user_id}", response_model=User)
def update(
    db: Session = Depends(get_db),
    *,
    user_id: int = Path(..., title="The ID of the user to update", ge=1),
    user_in: UserUpdate,
):
    usr = user.read(db, user_id=user_id)
    if not usr:
        raise HTTPException(
            status_code=404, detail="User not found",
        )
    usr = user.update(db, user=usr, user_in=user_in)
    return usr


@router.get("/{user_id}/favorite/hospitals", response_model=List[FavoriteHospital])
def read_favorite_hospitals(
    db: Session = Depends(get_db),
    *,
    user_id: int = Path(
        ..., title="The ID of the user to read favorite hospitals", ge=1
    ),
):
    usr = user.read(db, user_id=user_id)
    if not usr:
        raise HTTPException(
            status_code=404, detail="User not found",
        )
    return favorite.read_hospital_multi(db, user_id=user_id)


@router.post(
    "/{user_id}/favorite/hospitals/{hospital_id}", response_model=FavoriteHospital
)
def create_favorite_hospital(
    db: Session = Depends(get_db),
    *,
    user_id: int = Path(
        ...,
        title="The ID of the user to add the hospital to the favorite hospital list",
        ge=1,
    ),
    hospital_id: int = Path(
        ...,
        title="The ID of the hospital to be added to the user's favorite hospital list",
        ge=1,
    ),
):
    usr = user.read(db, user_id=user_id)
    if not usr:
        raise HTTPException(
            status_code=404, detail="User not found",
        )
    hosp = hospital.read(db, hospital_id=hospital_id)
    if not hosp:
        raise HTTPException(
            status_code=404, detail="Hospital not found",
        )
    return favorite.create_hospital(db, user_id=user_id, hospital_id=hospital_id)


@router.delete(
    "/{user_id}/favorite/hospitals/{hospital_id}",
    response_model=Optional[FavoriteHospital],
)
def delete_favorite_hospital(
    db: Session = Depends(get_db),
    *,
    user_id: int = Path(
        ...,
        title="The ID of the user to remove the hospital from the favorite hospital list",
        ge=1,
    ),
    hospital_id: int = Path(
        ...,
        title="The ID of the hospital to be removeded from the user's favorite hospital list",
        ge=1,
    ),
):
    usr = user.read(db, user_id=user_id)
    if not usr:
        raise HTTPException(
            status_code=404, detail="User not found",
        )
    hosp = hospital.read(db, hospital_id=hospital_id)
    if not hosp:
        raise HTTPException(
            status_code=404, detail="Hospital not found",
        )
    fav = favorite.read_hospital(db, user_id=user_id, hospital_id=hospital_id)
    if not fav:
        raise HTTPException(
            status_code=400,
            detail="The hospital is not in the favorite list of this user",
        )
    return favorite.delete_hospital(db, fav=fav)


@router.get("/{user_id}/favorite/shops", response_model=List[FavoriteShop])
def read_favorite_shops(
    db: Session = Depends(get_db),
    *,
    user_id: int = Path(..., title="The ID of the user to read favorite shops", ge=1),
):
    usr = user.read(db, user_id=user_id)
    if not usr:
        raise HTTPException(
            status_code=404, detail="User not found",
        )
    return favorite.read_shop_multi(db, user_id=user_id)


@router.post("/{user_id}/favorite/shops/{hospital_id}", response_model=FavoriteShop)
def create_favorite_shop(
    db: Session = Depends(get_db),
    *,
    user_id: int = Path(..., title="The ID of the user to read favorite shop", ge=1),
    shop_id: int = Path(
        ..., title="The ID of the shop to add as a favorite shop", ge=1
    ),
):
    usr = user.read(db, user_id=user_id)
    if not usr:
        raise HTTPException(
            status_code=404, detail="User not found",
        )
    shp = shop.read(db, shop_id=shop_id)
    if not shp:
        raise HTTPException(
            status_code=404, detail="Shop not found",
        )
    return favorite.create_shop(db, user_id=user_id, shop_id=shop_id)

@router.delete(
    "/{user_id}/favorite/shops/{shop_id}",
    response_model=Optional[FavoriteShop],
)
def delete_favorite_shop(
    db: Session = Depends(get_db),
    *,
    user_id: int = Path(
        ...,
        title="The ID of the user to remove the shop from one's favorite list",
        ge=1,
    ),
    shop_id: int = Path(
        ...,
        title="The ID of the shop to be removeded from the user's favorite list",
        ge=1,
    ),
):
    usr = user.read(db, user_id=user_id)
    if not usr:
        raise HTTPException(
            status_code=404, detail="User not found",
        )
    shp = shop.read(db, shop_id=shop_id)
    if not shp:
        raise HTTPException(
            status_code=404, detail="Shop not found",
        )
    fav = favorite.read_shop(db, user_id=user_id, shop_id=shop_id)
    if not fav:
        raise HTTPException(
            status_code=400,
            detail="The shop is not in the user's favorite list",
        )
    return favorite.delete_shop(db, fav=fav)

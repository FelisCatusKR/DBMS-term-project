from pydantic import *
from typing import List

from fastapi import APIRouter, Depends, Security, Path, HTTPException
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.api.utils.security import get_current_user
from app.crud import user
from app.models.user import User as DBUser
from app.schemas.user import User, UserCreate, UserRegister, UserUpdate

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

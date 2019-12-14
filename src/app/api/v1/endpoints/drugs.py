from pydantic import *
from typing import List, Optional

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.crud import drug
from app.schemas.drug import (
    Drug,
    DrugCreate,
    DrugUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[Drug])
def read_multi(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: Optional[int] = 0,
    limit: Optional[conint(le=100)] = 100,
):
    drugs = drug.read_multi_by_name(db, q=q, skip=skip, limit=limit)
    return drugs


@router.post("/", response_model=Drug)
def create(db: Session = Depends(get_db), *, drug_in: DrugCreate):
    drg = drug.create(db, drug=drug_in)
    return drg


@router.get("/{drug_id}", response_model=Drug)
def read(
    db: Session = Depends(get_db),
    drug_id: int = Path(..., title="The ID of the drug to read", ge=1),
):
    drg = drug.read(db, drug_id=drug_id)
    if drg is None:
        raise HTTPException(
            status_code=404, detail="Drug not found",
        )
    return drg


@router.put("/{drug_id}", response_model=Drug)
def update(
    db: Session = Depends(get_db),
    *,
    drug_id: int = Path(..., title="The ID of the drug to update", ge=1),
    drug_in: DrugUpdate,
):
    drg = drug.read(db, drug_id=drug_id)
    if drg is None:
        raise HTTPException(
            status_code=404, detail="Drug not found",
        )
    drg = drug.update(db, drug=drg, drug_in=drug_in)
    return drg

from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from app.crud import user
from app.api.utils.db import get_db

security = HTTPBasic()


def get_current_user(
    db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)
):
    cur_user = user.authenticate(
        db, email=credentials.username, password=credentials.password
    )
    if cur_user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return cur_user

from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import JWTDecodeError
from sqlalchemy.orm import Session

from app.crud import user
from app.api.utils.db import get_db
from app.core.jwt import ALGORITHM, SECRET_KEY
from app.core.security import OAuth2PasswordBearer
from app.models.user import User
from app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


def get_current_user(
    db: Session = Depends(get_db), token: str = Security(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except JWTDecodeError:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    user = user.get(db, user_id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

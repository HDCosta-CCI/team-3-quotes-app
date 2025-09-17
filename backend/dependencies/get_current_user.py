from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from dependencies.get_db import get_db
from models.users import Users
from dotenv import load_dotenv
import os
from uuid import UUID

oauth2_bearer = OAuth2PasswordBearer("auth/sign-in")

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

from fastapi.security import HTTPBearer

access_scheme  = HTTPBearer(auto_error=False, scheme_name="bearerAuth")
refresh_scheme = HTTPBearer(auto_error=False, scheme_name="refreshAuth")

def get_current_user(request: Request, db: Session = Depends(get_db)):
    claims = getattr(request.state, "auth", None)
    if not claims or not claims.get("sub"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    user_id = UUID(claims["user_id"])
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user

from fastapi import Depends, Request, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from dependencies.get_db import get_db
from models.users import Users
from dotenv import load_dotenv
import os
from uuid import UUID
from auth.token import validate_token

oauth2_bearer = OAuth2PasswordBearer("auth/sign-in")

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

from fastapi.security import HTTPBearer

access_scheme  = HTTPBearer(auto_error=False, scheme_name="bearerAuth")

def get_current_user(
    token=Depends(access_scheme),  # this will get HTTPAuthorizationCredentials or None
    db: Session = Depends(get_db)
):
    if token is None or token.credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        claims = validate_token(token.credentials)  # your function to decode and verify JW

        if not claims or not claims.get("first_name"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token claims")

        user_id = UUID(claims.get("user_id"))
    

        user = db.query(Users).filter(Users.user_id == user_id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        data = {
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        
        return data
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID in token")


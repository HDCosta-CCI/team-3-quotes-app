from fastapi import HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import timedelta, datetime
from uuid import UUID
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))



def create_access_token(
    email: str,
    first_name: str,
    user_id: UUID,
    refresh: bool = False,
    expire_delta: timedelta = None
):
    try:
        payload = {
            "sub": first_name,
            "email": email,
            "user_id": str(user_id),
            "refresh": refresh,
        }
        if expire_delta is not None:
            expires = datetime.utcnow() + expire_delta
        else:
            if refresh:
                expires = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
            else:
                expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        payload.update({"exp": expires})
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    except Exception as e:
        raise e
    
def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        first_name = payload.get("sub")
        email = payload.get("email")
        user_id = payload.get("user_id")
        return {'first_name': first_name, 'user_id': user_id, 'email': email}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token.')
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token has expired.')

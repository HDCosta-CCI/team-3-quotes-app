from fastapi import HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import timedelta, datetime
from uuid import UUID
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRY = 20

def create_access_token(email: str, first_name: str, user_id:UUID, expire_delta: timedelta = None, refresh: bool = False):
    try:
        encode = {"sub":first_name, "role": email, "user_id": str(user_id)}
        expires = datetime.utcnow() + (expire_delta if expire_delta is not None else timedelta(minutes=ACCESS_TOKEN_EXPIRY))
        encode.update({"exp": expires})
        encode.update({"refresh": refresh})
        token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    except JWTError:
        raise JWTError
    except Exception as e:
        return e 
    else:
        return token
    
def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        first_name = payload.get("sub")
        email = payload.get("role")
        user_id = payload.get("user_id")
        return {'first_name': first_name, 'user_id': user_id, 'email': email}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token.')
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token has expired.')

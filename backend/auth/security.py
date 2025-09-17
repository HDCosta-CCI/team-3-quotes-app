from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])

def hash_password(plain_password: str):
    try:
        hashed_password = bcrypt_context.hash(plain_password)
    except Exception:
        raise Exception
    else:
        return hashed_password

def verify_password(plain_password:str, hashed_password: str):
    try:
        check_password = bcrypt_context.verify(plain_password, hashed_password)
    except Exception:
        raise
    else:
        return check_password

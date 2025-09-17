from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from dependencies.get_db import get_db
from services.auth_services import AuthServices
from dto.user_dto import UserCreateRequest, UserSignInRequest

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
def sign_up(user_request: UserCreateRequest, db: Session = Depends(get_db)):
    try:
        return AuthServices(db).user_sign_up(user_request)
    except Exception as e:
        raise e
    
@router.post("/sign-in", status_code=status.HTTP_200_OK)
def sign_in(user_request: UserSignInRequest, db: Session = Depends(get_db)):
    try:
        return AuthServices(db).user_sign_in(user_request)
    except Exception as e:
        raise e
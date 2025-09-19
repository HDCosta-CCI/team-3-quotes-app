from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from dependencies.get_db import get_db
from services.auth_services import AuthServices
from dto.response_dto import GlobalResponse
from dto.user_dto import UserCreateRequest, UserSignInRequest

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
refresh_scheme = HTTPBearer(auto_error=False, scheme_name="refreshAuth")

@router.post("/sign-up", status_code=status.HTTP_201_CREATED, openapi_extra={"security": []})
def sign_up(user_request: UserCreateRequest, db: Session = Depends(get_db)):
    try:
        data = AuthServices(db).user_sign_up(user_request)

        return GlobalResponse(
            data = data,
            message = "User created successfully",
            success =True
        )
    
    except Exception as e:
        raise e
    
@router.post("/sign-in", status_code=status.HTTP_200_OK, openapi_extra={"security": []})
def sign_in(user_request: UserSignInRequest, db: Session = Depends(get_db)):
    try:
        data = AuthServices(db).user_sign_in(user_request)

        return GlobalResponse(
            data = data,
            message = "User created successfully",
            success=True
        )
    
    except Exception as e:
        raise e
    

@router.post("/refresh-token")
def create_token(refresh_token= Depends(refresh_scheme), db: Session = Depends(get_db)):
    try:
        data = AuthServices(db).refresh_access(refresh_token)

        return GlobalResponse(
            data = data,
            message = "Access token and refresh token generated.",
            success=True
        )
    
    except Exception as e:
        raise e
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from dto.user_dto import UserUpdateRequest
from dependencies.get_db import get_db
from dependencies.get_current_user import get_current_user
from services.user_services import UserServices

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
  
@router.get("")
def fetch_users(user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return UserServices(db).fetch_user_details(user)
    except Exception as e:
        raise e
    
@router.patch("")
def update_user(user_update_request: UserUpdateRequest, user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return UserServices(db).update_user_details(user, user_update_request)
    except Exception as e:
        raise e
    
@router.patch("/{user_id}")
def delete_user(user_id: UUID, user = Depends(get_current_user), db: Session = Depends(get_db)):
    return UserServices(db).delete_user(user_id)
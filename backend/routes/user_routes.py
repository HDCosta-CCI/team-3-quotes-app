from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from dto.response_dto import GlobalResponse
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
        data = UserServices(db, user=None).fetch_user_details(user)
        return GlobalResponse(
            data= data,
            message= "User fetched successfully",
            success= True
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
    
@router.patch("")
def update_user(user_update_request: UserUpdateRequest, user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        data = UserServices(db, user).update_user_details( user_update_request)
        return GlobalResponse(
            data= data,
            message= "User updated successfully",
            success= True
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
    
@router.patch("/{user_id}")
def delete_user(user_id: UUID, user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        data =  UserServices(db, user).delete_user(user_id)
        return GlobalResponse(
                data= data,
                message= "User deleted successfully",
                success= True
            )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
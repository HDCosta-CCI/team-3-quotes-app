from fastapi import HTTPException, status
from dto.user_dto import UserUpdateRequest
from models.users import Users

class UserServices:
    def __init__(self, db):
        self.db = db

    def fetch_user_details(self, user):
        try:
            user = self.db.query(Users).filter(Users.user_id == user.user_id).first()
            return {
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        except HTTPException as e:
            raise e
    
    def update_user_details(self, user, user_update_request: UserUpdateRequest):
        try:
            user = self.db.query(Users).filter(Users.user_id == user.user_id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found.")
    
            update_user = user_update_request.model_dump(exclude_unset=True)
            self.db.query(Users).filter(Users.user_id == user.user_id).update(update_user)

            self.db.commit()
            self.db.refresh(user)

            
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        else:
            return {"message" : "Updated successfully", "user": user}


    def delete_user(self, user_id):
        try:
            user = self.db.query(Users).filter(Users.user_id == user_id).first()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found.")
            
            updated_user = self.db.query(Users).filter(Users.user_id == user.user_id).update({Users.status : "inactive"})

            self.db.commit()

        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        else:
            return {"message" : "Deleted successfully"}

        
        

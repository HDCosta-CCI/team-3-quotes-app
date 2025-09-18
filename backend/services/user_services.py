from fastapi import HTTPException, status
from dto.user_dto import UserUpdateRequest
from models.users import Users

class UserServices:
    def __init__(self, db, user):
        self.db = db
        self.user = user

    def fetch_user_details(self, user):
        try:
            user = self.db.query(Users).filter(Users.user_id == user.user_id).first()

            data = {
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
            
        except HTTPException as e:
            raise e
        except Exception as e:
            raise e
        else:
            return data
    
    def update_user_details(self, user_update_request: UserUpdateRequest):
        try:
            user = self.db.query(Users).filter(Users.user_id == self.user.user_id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found.")
    
            update_user = user_update_request.model_dump(exclude_unset=True)
            self.db.query(Users).filter(Users.user_id == user.user_id).update(update_user)

            self.db.commit()
            self.db.refresh(user)

            data = {
                'id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }

        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        else:
            return data


    def delete_user(self, user_id):
        try:
            user = self.db.query(Users).filter(Users.user_id == user_id).first()

            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found.")
            
            self.db.query(Users).filter(Users.user_id == user.user_id).update({Users.status : "inactive"})
            self.db.commit()

            data = {}

        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        else:
            return data

        
        

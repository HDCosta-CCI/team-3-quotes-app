from fastapi import HTTPException, status
from datetime import timedelta
from auth.security import hash_password, verify_password
from auth.token import create_access_token, validate_token
from dto.user_dto import UserCreateRequest, UserSignInRequest
from models.users import Users

class AuthServices:
    def __init__(self, db):
        self.db = db

    def user_sign_up(self, user_create_request: UserCreateRequest):
        try:
            user = self.db.query(Users).filter(Users.email == user_create_request.email).first()
            if user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist.")

            new_user = Users(
                first_name = user_create_request.first_name,
                last_name = user_create_request.last_name,
                email = user_create_request.email,
                password = hash_password(user_create_request.password),
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            data = {
                'id': new_user.user_id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }
            return data

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        


    def user_sign_in(self, user_sign_in_request: UserSignInRequest):
        try:
            user = self.db.query(Users).filter(Users.email == user_sign_in_request.email).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email does not exist.")
            
            if not verify_password(user_sign_in_request.password, user.password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password.")
            
            access_token = create_access_token(first_name=user.first_name, email=user.email, user_id=user.user_id )
            refresh_token = create_access_token(first_name=user.first_name, email=user.email, user_id=user.user_id, expire_delta=timedelta(days=1), refresh=True)

            data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'bearer'
            }
            return data

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")

        

    def refresh_access(self, refresh_token):
        try:
            if not refresh_token:
                raise HTTPException(status_code=401, detail="Missing refresh token")
            
            user_data = validate_token(refresh_token)
            
            if not user_data:
                raise HTTPException(status_code=403, detail="Invalid refresh token")
            
            new_access_token = create_access_token(
                first_name=user_data['first_name'],
                email=user_data['email'],
                user_id=user_data['user_id']
            )
            new_refresh_token = create_access_token(first_name=user_data['first_name'], email=user_data['email'], user_id=user_data['user_id'] , expire_delta=timedelta(days=1), refresh=True )

            data = {
                'access_token': new_access_token,
                'refresh_token': new_refresh_token,
                'token_type': 'bearer'
            }
            return data
        
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

from fastapi import HTTPException, status
from dto.user_dto import UserUpdateRequest
from models.users import Users
from models.quotes import Quotes
from models.user_quote_reactions import UserQuoteReactions

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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
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

        
    def fetch_quotes(self, user_id):
        try:
            quotes = self.db.query(Quotes).filter(Quotes.user_id == user_id).all()

            if not quotes:
                HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors not found.")

            quotes_list = []

            for q in quotes:
                quotes_list.append({
                    "quote": q.quote,
                    "author": q.author,
                    "likes": q.like,
                    "dislikes": q.dislike,
                    "tags": q.tags,
                    "user_id": str(q.user_id),
                    "quote_id": q.quote_id
                })

        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        else:
            return quotes_list

    def fetch_quotes_disliked(self, user_id):
        try:
            quotes =  self.db.query(Quotes, UserQuoteReactions).join(UserQuoteReactions, Quotes.quote_id == UserQuoteReactions.quote_id).filter(UserQuoteReactions.user_id == user_id, UserQuoteReactions.dislike == True).all()

            if not quotes:        
                HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors not found.")

            quotes_list = []
            
            for q in quotes:
                quotes_list.append({
                    "quote": q.quote,
                    "author": q.author,
                    "likes": q.like,
                    "dislikes": q.dislike,
                    "tags": q.tags,
                    "user_id": str(q.user_id),
                    "quote_id": q.quote_id
                })

        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        else:
            return quotes_list
        

    def fetch_quotes_liked(self, user_id):
        try:
            quotes =  self.db.query(Quotes).join(UserQuoteReactions, Quotes.quote_id == UserQuoteReactions.quote_id).filter(UserQuoteReactions.user_id == user_id, UserQuoteReactions.like == True).all()

            if not quotes:        
                HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors not found.")

            quotes_list = []
            
            for q in quotes:
                quotes_list.append({
                    "quote": q.quote,
                    "author": q.author,
                    "likes": q.like,
                    "dislikes": q.dislike,
                    "tags": q.tags,
                    "user_id": str(q.user_id),
                    "quote_id": q.quote_id
                })

        except HTTPException as e:
            raise e
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        else:
            return quotes_list
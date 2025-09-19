from fastapi import HTTPException, status
from dto.user_dto import UserUpdateRequest
from models.users import Users
from models.quotes import Quotes
from models.user_quote_reactions import UserQuoteReactions

class UserServices:
    def __init__(self, db, user):
        self.db = db
        self.user = user

    def fetch_user_details(self):
        try:
            self._is_authenticate_user()
            user = self.db.query(Users).filter(Users.user_id == self.user.get("user_id")).first()

            data = self.format_data(user)
            
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        else:
            return data
    
    def update_user_details(self, user_update_request: UserUpdateRequest):
        try:
            self._is_authenticate_user()
            user = self._check_user_exist(self.user.get("user_id"))

            update_user = user_update_request.model_dump(exclude_unset=True)
            self.db.query(Users).filter(Users.user_id == user.user_id).update(update_user)

            self.db.commit()
            self.db.refresh(user)

            data = self.format_data(user)

        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        else:
            return data


    def delete_user(self, user_id):
        try:
            self._is_authenticate_user()
            user = self._check_user_exist(user_id)
            
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
            self._is_authenticate_user()
            quotes = self.db.query(Quotes).filter(Quotes.user_id == user_id).all()

            if not quotes:
                HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors not found.")

            quotes_list = self.format_quotes(quotes)

        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        else:
            return quotes_list

    def fetch_quotes_disliked(self, user_id):
        try:
            self._is_authenticate_user()
            quotes =  self.db.query(Quotes, UserQuoteReactions).join(UserQuoteReactions, Quotes.quote_id == UserQuoteReactions.quote_id).filter(UserQuoteReactions.user_id == user_id, UserQuoteReactions.dislike == True).all()

            if not quotes:        
                HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors not found.")

            quotes_list = []
            
            quotes_list = self.format_quotes(quotes)

        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        else:
            return quotes_list
        

    def fetch_quotes_liked(self, user_id):
        try:
            self._is_authenticate_user()
            quotes =  self.db.query(Quotes).join(UserQuoteReactions, Quotes.quote_id == UserQuoteReactions.quote_id).filter(UserQuoteReactions.user_id == user_id, UserQuoteReactions.like == True).all()

            if not quotes:        
                HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authors not found.")

            quotes_list = self.format_quotes(quotes)

        except HTTPException as e:
            raise e
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        else:
            return quotes_list
        
    def _is_authenticate_user(self):
        if not self.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed!"
            )
    
    def _check_user_exist(self, user_id):
        try:
            user = self.db.query(Users).filter(Users.user_id == user_id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
            return user
        except Exception as e:
            raise e
        
    def format_quotes(self, quotes):
        quotes_list = []
        for quote in quotes:
            quotes_list.append({
                "quote": quote.quote,
                "author": quote.author,
                "likes": quote.like,
                "dislikes": quote.dislike,
                "tags": quote.tags,
                "user_id": str(quote.user_id),
                "quote_id": quote.quote_id
            })
       
        return quotes_list
   
    def format_data(self, user):
        data = {
                'id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
       
        return data          
 
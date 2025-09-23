from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from dto.quotes_dto import QuoteRequest, QuoteUpdateRequest
from models.quotes import Quotes
from models.users import Users
from models.user_quote_reactions import UserQuoteReactions
import time

class QuoteServices:
    def __init__(self, db: Session, user):
        self.db = db
        self.user = user


    def get_all_quotes(self):
        try:
            quotes = self.db.query(Quotes).all()
            if not quotes:
                return []

            quotes_list = []
            for quote in quotes:
                quotes_list.append({
                    "user_id": quote.user_id,
                    "quote_id": quote.quote_id,
                    "quote": quote.quote,
                    "author": quote.author,
                    "likes": quote.like,
                    "dislikes": quote.dislike,
                    "tags": quote.tags,
                })
            return quotes_list
        
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")



    def get_quote(self, quote_id):
        try:
            self._is_authenticate_user()
            quote = self._check_quote_exist(quote_id)
            
            data = self._format_quote(quote)
            return data

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        


    def get_quote_tags(self): 
        try:
            self._is_authenticate_user()
            tags = self.db.query(Quotes.tags).all()

            tag_set = set()
            for (tag_string,) in tags:
                if tag_string:
                    for tag in tag_string.split(";"):
                        tag_set.add(tag.strip())

            sorted_tags = sorted(tag_set)
            return sorted_tags

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")



    def create_quote(self, request: QuoteRequest) -> Quotes:
        try:
            self._is_authenticate_user()
            
            new_quote = Quotes(
                quote = request.quote,
                author = request.author,
                tags = request.tags,
                user_id = self.user.get("user_id")
            )
            self.db.add(new_quote)
            self.db.commit()
            self.db.refresh(new_quote)
            
            return {
                "quote_id": new_quote.quote_id,
                "quote" : new_quote.quote, 
                "author": new_quote.author,
                "tags": new_quote.tags,
            }
        
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        


    def update_quote(self, quote_id, request: QuoteUpdateRequest):
        try:
            self._is_authenticate_user()
            quote = self._check_quote_exist(quote_id)
            
            updated_data = request.model_dump(exclude_unset=True)
            for key, value in updated_data.items():
                setattr(quote, key, value)
            
            self.db.commit()
            self.db.refresh(quote)

            data = self._format_quote(quote)
            return data

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")



    def delete_quote(self, quote_id):
        try:
            self._is_authenticate_user()
            quote = self._check_quote_exist(quote_id)
            
            self.db.query(Quotes).filter(Quotes.quote_id == quote_id).delete()
            self.db.commit()
            return {
                "entries" : None,
            }
    
        except HTTPException as e:
            raise e    
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")



    def like_quote_up(self, quote_id):
        try:
            self._is_authenticate_user()
            quote = self._check_quote_exist(quote_id)
            self._is_self_reaction(quote.user_id, self.user.get("user_id"))
            reaction = self._check_reaction_exist(quote.quote_id, self.user.get("user_id"))
            
            if reaction:
                if reaction.like:
                    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Already liked!")
                else:
                    if reaction.dislike:
                        reaction.like = True
                        reaction.dislike = False
                    else:
                        reaction.like = True
            else:
                reaction = UserQuoteReactions(
                    like=True,
                    dislike=False,
                    quote_id=quote.quote_id,
                    user_id=self.user.get("user_id")
                )
                self.db.add(reaction)
            self.db.commit()
            self.db.refresh(quote)
            self.db.refresh(reaction)

            data = self._format_quote(quote)
            return data
        
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")



    def dislike_quote_up(self, quote_id):
            try:
                self._is_authenticate_user()
                quote = self._check_quote_exist(quote_id)
                self._is_self_reaction(quote.user_id, self.user.get("user_id"))
                reaction = self._check_reaction_exist(quote.quote_id, self.user.get("user_id"))
                
                if reaction:
                    if reaction.dislike:
                        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Already disliked!")
                    else:
                        if reaction.like:
                            reaction.dislike = True
                            reaction.like = False
                        else:
                            reaction.dislike = True
                else:
                    reaction = UserQuoteReactions(
                        like=False,
                        dislike=True,
                        quote_id=quote.quote_id,
                        user_id=self.user.get("user_id")
                    )
                    self.db.add(reaction)
                self.db.commit()
                self.db.refresh(quote)
                self.db.refresh(reaction)

                data = self._format_quote(quote)
                return  data
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")



    def like_quote_down(self, quote_id):
        try:
            self._is_authenticate_user()
            quote = self._check_quote_exist(quote_id)
            self._is_self_reaction(quote.user_id, self.user.get("user_id"))
            reaction = self._check_reaction_exist(quote.quote_id, self.user.get("user_id"))
            
            if reaction:
                if not reaction.like:
                    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Quote was not liked!")
                else:
                    self.db.query(UserQuoteReactions).filter(UserQuoteReactions.reaction_id == reaction.reaction_id).delete(synchronize_session=False)
            else:
                raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Quote was not liked!")
            self.db.commit()
            self.db.refresh(quote)

            data = self._format_quote(quote)
            return  data
        
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")



    def dislike_quote_down(self, quote_id):
        try:
            self._is_authenticate_user()
            quote = self._check_quote_exist(quote_id)
            self._is_self_reaction(quote.user_id, self.user.get("user_id"))
            reaction = self._check_reaction_exist(quote.quote_id, self.user.get("user_id"))
            
            if reaction:
                if not reaction.dislike:
                    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Quote was not disliked!")
                else:
                    self.db.query(UserQuoteReactions).filter(UserQuoteReactions.reaction_id == reaction.reaction_id).delete(synchronize_session=False)
            else:
                raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Quote was not disliked!")
            self.db.commit()
            self.db.refresh(quote)

            return  
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        

    
    def fetch_liked_user(self, quote_id):
        try:
            self._is_authenticate_user()
            users = self.db.query(Users).join(UserQuoteReactions, UserQuoteReactions.user_id == Users.user_id).filter(UserQuoteReactions.quote_id == quote_id, UserQuoteReactions.like == True).all()

            data = []
            for user in users:
                data.append({
                    'first_name': user.first_name,
                    'last_name': user.last_name
                })
            return data
        
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        


    def fetch_disliked_user(self, quote_id):
        try:
            self._is_authenticate_user()
            users = self.db.query(Users).join(UserQuoteReactions, UserQuoteReactions.user_id == Users.user_id).filter(UserQuoteReactions.quote_id == quote_id, UserQuoteReactions.dislike == True).all()

            data = []
            for user in users:
                data.append({
                    'first_name': user.first_name,
                    'last_name': user.last_name
                })
            return data
        
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        


    def count_like_dislike(self):
        time.sleep(1)

        try:
            quotes = self.db.query(Quotes).all()
            for quote in quotes:
                like_count = self.db.query(func.count()).filter(
                    UserQuoteReactions.quote_id == quote.quote_id,
                    UserQuoteReactions.like == True
                ).scalar()

                dislike_count = self.db.query(func.count()).filter(
                    UserQuoteReactions.quote_id == quote.quote_id,
                    UserQuoteReactions.dislike == True
                ).scalar()

                quote.like = like_count
                quote.dislike = dislike_count
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500,detail=f"Internal server error: {str(e)}")

        




    # Helper functions

    def _is_authenticate_user(self):
        if not self.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication Failed!"
            )

    def _check_quote_exist(self, quote_id):
        try:
            quote = self.db.query(Quotes).filter(Quotes.quote_id == quote_id).first()
            if not quote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found.")
            return quote
        except Exception as e:
            raise e
        
    def _is_self_reaction(self, quote_user_id, user_id):
        if quote_user_id == user_id:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Cannot like/dislike own quotes!")
        
    def _check_reaction_exist(self, quote_id, user_id):
        try:
            reaction = self.db.query(UserQuoteReactions).filter(UserQuoteReactions.quote_id == quote_id, UserQuoteReactions.user_id == user_id).first()
            return reaction
        except Exception as e:
            raise e
        

    def _format_quote(self, quote):
        data = {
                "id": str(quote.quote_id),
                "quote": quote.quote,
                "author": quote.author,
                "like": quote.like,
                "dislike": quote.dislike,
                "tags": quote.tags
            }
        
        return data
    
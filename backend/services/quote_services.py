from typing import Any, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from dto.quotes_dto import QuoteRequest, QuoteUpdateRequest
from models.quotes import Quotes
from models.users import Users
from models.user_quote_reactions import UserQuoteReactions
from uuid import UUID

class QuoteServices:
    def __init__(self, db: Session, user):
        self.db = db
        self.user = user

    def get_all_quotes(self):
        try:
            quotes = self.db.query(Quotes).all()
            if not quotes:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Quotes found!")
            print(quotes)

            quotes_list = []

            for quote in quotes:
                quotes_list.append({
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
            self.authorize_user()
            quote = self.db.query(Quotes).filter(Quotes.quote_id == quote_id).first()
            if not quote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
            
            data = {
                "id": str(quote.quote_id),
                "quote": quote.quote,
                "author": quote.author,
                "like": quote.like,
                "dislike": quote.dislike,
                "tags": quote.tags,
            }
            return data

        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        

    def get_quote_tags(self): 
        try:
            if not self.user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized.")
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
            if self.user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed!")

            new_quote = Quotes(
                quote = request.quote,
                author = request.author,
                tags = request.tags,
                user_id = self.user.user_id
            )
            self.db.add(new_quote)
            self.db.commit()
            self.db.refresh(new_quote)
            
            return {
                "quote" : new_quote.quote, 
                "author": new_quote.author,
                "tags": new_quote.tags,
                "user_id": self.user.user_id
            }
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        

    def update_quote(self, quote_id, request: QuoteUpdateRequest):
        try:
            if not self.user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized.")
            quote = self.db.query(Quotes).filter(Quotes.quote_id == quote_id).first()
            if not quote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
            
            updated_data = request.model_dump(exclude_unset=True)
            for key, value in updated_data.items():
                setattr(quote, key, value)
            
            self.db.commit()
            self.db.refresh(quote)

            data = {
                "id": str(quote.quote_id),
                "quote": quote.quote,
                "author": quote.author,
                "like": quote.like,
                "dislike": quote.dislike,
                "tags": quote.tags,
            }

            return data

        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")


    def delete_quote(self, quote_id):
        try:
            if not self.user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized.")
            quote = self.db.query(Quotes).filter(Quotes.quote_id == quote_id).first()
            if not quote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
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
            if not self.user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized.")
            
            quote = self.db.query(Quotes).filter(Quotes.quote_id == quote_id).first()
            if not quote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found.")
            
            if quote.user_id == self.user.user_id:
                raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Cannot like own quotes!")
            
            reaction = self.db.query(UserQuoteReactions).filter(UserQuoteReactions.quote_id==quote_id, UserQuoteReactions.user_id==self.user.user_id).first()
            
            if reaction:
                if reaction.like:
                    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Already liked!")
                else:
                    if reaction.dislike:
                        quote.dislike -= 1
                        quote.like += 1
                        reaction.like = True
                        reaction.dislike = False
                    else:
                        quote.like += 1
                        reaction.like = True
            else:
                reaction = UserQuoteReactions(
                    like=True,
                    dislike=False,
                    quote_id=quote.quote_id,
                    user_id=self.user.user_id
                )
                self.db.add(reaction)
                quote.like += 1
            
            self.db.commit()
            self.db.refresh(quote)
            self.db.refresh(reaction)

            return  {
                "id": reaction.reaction_id,
                "quote": quote.quote,
                "author": quote.author,
                "like": quote.like,
                "dislike": quote.dislike,
                "tags": quote.tags
            }
                
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")


    def dislike_quote_up(self, quote_id):
            try:
                if not self.user:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized.")
                
                quote = self.db.query(Quotes).filter(Quotes.quote_id == quote_id).first()
                if not quote:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found.")
                
                if quote.user_id == self.user.user_id:
                    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Cannot dislike own quotes!")
                
                reaction = self.db.query(UserQuoteReactions).filter(UserQuoteReactions.quote_id==quote_id, UserQuoteReactions.user_id==self.user.user_id).first()

                
                if reaction:
                    if reaction.dislike:
                        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Already disliked!")
                    else:
                        if reaction.like:
                            quote.like -= 1
                            quote.dislike += 1
                            reaction.dislike = True
                            reaction.like = False
                        else:
                            quote.dislike += 1
                            reaction.dislike = True
                else:
                    reaction = UserQuoteReactions(
                        like=False,
                        dislike=True,
                        quote_id=quote.quote_id,
                        user_id=self.user.user_id
                    )
                    self.db.add(reaction)
                    quote.dislike += 1
                
                self.db.commit()
                self.db.refresh(quote)
                self.db.refresh(reaction)

                return  {
                    "id": reaction.reaction_id,
                    "quote": quote.quote,
                    "author": quote.author,
                    "like": quote.like,
                    "dislike": quote.dislike,
                    "tags": quote.tags
                }
                    
            except HTTPException as e:
                raise e
        
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")


    def like_quote_down(self, quote_id):
        try:
            if not self.user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized.")
            
            quote = self.db.query(Quotes).filter(Quotes.quote_id == quote_id).first()
            if not quote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found.")
            
            if quote.user_id == self.user.user_id:
                raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Cannot like/dislike own quotes!")
            
            reaction = self.db.query(UserQuoteReactions).filter(UserQuoteReactions.quote_id==quote_id, UserQuoteReactions.user_id==self.user.user_id).first()
            
            if reaction:
                if not reaction.like:
                    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Quote was not liked!")
                else:
                    quote.like -= 1
                    self.db.query(UserQuoteReactions).filter(UserQuoteReactions.reaction_id == reaction.reaction_id).delete(synchronize_session=False)

            self.db.commit()
            self.db.refresh(quote)

            return  {
                "id": quote.quote_id,
                "quote": quote.quote,
                "author": quote.author,
                "like": quote.like,
                "dislike": quote.dislike,
                "tags": quote.tags
            }
                
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")


    def dislike_quote_down(self, quote_id):
        try:
            if not self.user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized.")
            
            quote = self.db.query(Quotes).filter(Quotes.quote_id == quote_id).first()
            if not quote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found.")
            
            if quote.user_id == self.user.user_id:
                raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Cannot like/dislike own quotes!")
            
            reaction = self.db.query(UserQuoteReactions).filter(UserQuoteReactions.quote_id==quote_id, UserQuoteReactions.user_id==self.user.user_id).first()
            
            if reaction:
                if not reaction.dislike:
                    raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Quote was not disliked!")
                else:
                    quote.dislike -= 1
                    self.db.query(UserQuoteReactions).filter(UserQuoteReactions.reaction_id == reaction.reaction_id).delete(synchronize_session=False)

            self.db.commit()
            self.db.refresh(quote)

            return  {
                "id": quote.quote_id,
                "quote": quote.quote,
                "author": quote.author,
                "like": quote.like,
                "dislike": quote.dislike,
                "tags": quote.tags
            }
                
        except HTTPException as e:
            raise e
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {e}")
        
    
    def fetch_liked_user(self, quote_id):
        try:
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
        
    def authorize_user(self):
        if not self.user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized!")

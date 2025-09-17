from typing import Any, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from dto.quotes_dto import QuoteRequest, QuoteUpdateRequest
from models.quotes import Quotes
from uuid import UUID

class QuoteServices:
    def __init__(self, db: Session):
        self.db = db

    def get_all_quotes(self):
        try:
            quotes = self.db.query(Quotes).all()
            if not quotes:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Quotes found!")
            return quotes
        
        except HTTPException as e:
            raise e


    def get_quote(self, quote_id):
        try:
            quote = self.db.query(Quotes).filter(Quotes.quotes_id == quote_id).first()
            if not quote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
            return quote

        except HTTPException as e:
            raise e
        

    def get_quote_tags(self): 
        try:
            quotes = self.db.query(Quotes).all()
            tag_set = set()

            for quote in quotes:
                if quote.tags:
                    for tag in quote.tags.split(";"):
                        tag_set.add(tag.strip())
            sorted_tags = sorted(tag_set)

            return {"tags": sorted_tags}
        except HTTPException as e:
            raise e

    def create_quote(self, request: QuoteRequest) -> Quotes:
        try:
            # if self.user is None:
            #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed!")

            new_quote = Quotes(**request.model_dump())
            self.db.add(new_quote)
            self.db.commit()
            self.db.refresh(new_quote)
            
            return {
                "quote" : new_quote.quote, 
                "author": new_quote.author,
                "tags": new_quote.tags,
                "user_id": new_quote.user_id
            }
        except HTTPException as e:
            raise e
        

    def update_quote(self, quote_id, request: QuoteUpdateRequest):
        try:
            quote = self.db.query(Quotes).filter(Quotes.quotes_id == quote_id).first()
            if not quote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
            
            updated_data = request.model_dump(exclude_unset=True)
            for key, value in updated_data.items():
                setattr(quote, key, value)
            
            self.db.commit()
            self.db.refresh(quote)

            return quote

        except HTTPException as e:
            raise e


    def delete_quote(self, quote_id):
        try:
            # if self.user is None:
            #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed!")

            quote = self.db.query(Quotes).filter(Quotes.quotes_id == quote_id).first()
            if not quote:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quote not found")
            self.db.query(Quotes).filter(Quotes.quotes_id == quote_id).delete()
            self.db.commit()
            return {
                "entries" : None,
            }
        except HTTPException as e:
            raise e


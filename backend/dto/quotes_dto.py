from typing import Any, List, Optional
from pydantic import BaseModel, Field
from uuid import UUID

class QuoteRequest(BaseModel):
    quote: str = Field(min_length=5)
    author: str = Field(min_length=5)
    tags: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "quote": "quote",
                "author": "author",
                "tags": "tag1;tag2",
            }
        },
        "from_attributes": True
    }

class Quote(BaseModel):
    quote_id: UUID
    quote: str = Field(min_length=5, max_length=255)
    author: str = Field(min_length=5, max_length=100)
    like: int = 0
    dislike: int = 0
    tags: Optional[str] = None
    user_id: UUID

    model_config = {
        "from_attributes": True
    }

class QuoteResponse(BaseModel):
    message: str = Field(min_length=5)
    success: bool = Field(default=True)
    data: List[Quote] | Quote | dict | dict[str, Any]
    
class QuoteUpdateRequest(BaseModel):
    quote: Optional[str] = None
    author: Optional[str] = None
    like: Optional[int] = None
    dislike: Optional[int] = None
    tags: Optional[str] = None



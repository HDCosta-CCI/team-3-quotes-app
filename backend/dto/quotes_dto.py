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
    
class QuoteUpdateRequest(BaseModel):
    quote: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[str] = None



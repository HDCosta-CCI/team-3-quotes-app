from typing import List, Optional
from pydantic import BaseModel, Field

class GlobalResponse(BaseModel):
    message: str = Field(min_length=5)
    success: bool
    data: List | dict | None
    errors: Optional[List] = None
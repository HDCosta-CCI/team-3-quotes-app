from typing import List
from pydantic import BaseModel, Field

class GlobalResponse(BaseModel):
    message: str = Field(min_length=5)
    success: bool = Field(default=True)
    data: List | dict
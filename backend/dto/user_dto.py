from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreateRequest(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    email: EmailStr
    password: str 

class UserSignInRequest(BaseModel):
    email: EmailStr
    password: str

class UserUpdateRequest(BaseModel):
    first_name : Optional[str] = Field(None, min_length=5, max_length=30)
    last_name : Optional[str] = Field(None, min_length=5, max_length=30)
    email : Optional[EmailStr] = Field(None)
    password : Optional[str] = Field(None)

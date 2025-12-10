from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: str
    full_name: str
    email: EmailStr

class AuthUser(BaseModel):
    email: EmailStr
    password: str
class AuthPublic(UserRead):
    acess_token: str
    token_type: str = "bearer"
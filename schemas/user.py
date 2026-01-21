from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    released: datetime
    year: int

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    released: datetime
    year: int
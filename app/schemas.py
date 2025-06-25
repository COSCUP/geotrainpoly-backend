from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    unknown = "unknown"

class RoleEnum(str, Enum):
    ATTENDEE = "ATTENDEE"
    STAFF = "STAFF"
    ADMIN = "ADMIN"

class UserRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    gender: GenderEnum
    role: RoleEnum
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    gender: Optional[GenderEnum] = None
    role: Optional[RoleEnum] = RoleEnum.ATTENDEE

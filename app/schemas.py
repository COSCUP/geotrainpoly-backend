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

class VisitTypeEnum(str, Enum):
    BOOTH = "BOOTH"   # 使用者被攤位掃（被動）
    OTHER = "OTHER"   # 使用者主動掃（主動）

class UserRead(BaseModel):
    id: str
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

class BoothRead(BaseModel):
    id: UUID
    name: str
    description: str
    points: int
    created_at: datetime

    class Config:
        orm_mode = True

class BoothCreate(BaseModel):
    name: str
    description: str
    points: int

class VisitRead(BaseModel):
    id: int
    user_id: str
    type: VisitTypeEnum
    booth_id: str
    message: Optional[str] = None
    visit_at: datetime

    class Config:
        orm_mode = True

# class VisitCreate(BaseModel):
#     user_id: str
#     type: VisitTypeEnum
#     booth_id: str
#     message: str

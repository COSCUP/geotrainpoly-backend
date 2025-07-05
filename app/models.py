import uuid
from sqlalchemy import Column, String, Integer, DateTime, Enum as PgEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from enum import Enum as PyEnum

from app.database import Base

class GenderEnum(PyEnum):
    male = "male"
    female = "female"
    unknown = "unknown"

class RoleEnum(PyEnum):
    ATTENDEE = "ATTENDEE"
    STAFF = "STAFF"
    ADMIN = "ADMIN"

class VisitTypeEnum(PyEnum):
    BOOTH = "BOOTH"   # 使用者被攤位掃（被動）
    OTHER = "OTHER"   # 使用者主動掃（主動）

class User(Base):
    __tablename__ = "users"

    id = Column(String(100), primary_key=True, index=True)  # save token from OPASS
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    gender = Column(PgEnum(GenderEnum, name="gender_enum"), nullable=True)
    role = Column(PgEnum(RoleEnum, name="role_enum"), default=RoleEnum.ATTENDEE, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

class Booth(Base):
    __tablename__ = "booths"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    points = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

class Visit(Base):
    __tablename__ = "visits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    type = Column(PgEnum(VisitTypeEnum, name="visit_enum"), nullable=False)
    booth_id = Column(UUID(as_uuid=True), nullable=True)
    message = Column(String, nullable=True)
    visit_at = Column(DateTime, server_default=func.now(), nullable=False)

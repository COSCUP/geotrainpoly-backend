import uuid
from sqlalchemy import Column, String, DateTime, Enum as PgEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from enum import Enum as PyEnum

Base = declarative_base()

class GenderEnum(PyEnum):
    male = "male"
    female = "female"
    unknown = "unknown"

class RoleEnum(PyEnum):
    ATTENDEE = "ATTENDEE"
    STAFF = "STAFF"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    gender = Column(PgEnum(GenderEnum, name="gender_enum"), nullable=True)
    role = Column(PgEnum(RoleEnum, name="role_enum"), default=RoleEnum.ATTENDEE, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

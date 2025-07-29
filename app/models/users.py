from sqlalchemy import Column, Integer, Text, Enum, String
from sqlalchemy.orm import relationship
from app.database import engine, Base
from app.models.achievements import Achievement


class User(Base):
    __tablename__ = "users"
    user_id = Column(String(40), primary_key=True)
    name = Column(Text)
    avatar = Column(Text)
    title = Column(Text)
    points = Column(Integer, server_default="0")

    achievements = relationship("Achievement", back_populates="owner")
    booths = relationship("UserBooths", back_populates="owner")

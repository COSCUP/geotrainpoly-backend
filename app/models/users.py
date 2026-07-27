from sqlalchemy import Column, Integer, Text, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(String(40), primary_key=True)
    name = Column(Text)
    reward = Column(Boolean, server_default="0")
    title = Column(Text)
    points = Column(Integer, server_default="0")

    achievements = relationship("UserAchievement", back_populates="owner")
    booths = relationship("UserBooths", back_populates="owner")
    msg = relationship("Msg", back_populates="owner")

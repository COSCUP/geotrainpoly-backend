from sqlalchemy import Column, Integer, Text, Enum, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import engine, Base


class Achievement(Base):
    __tablename__ = "achievements"
    achievement_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text)
    title = Column(Text)
    points = Column(Integer)
    user_id = Column(String(36), ForeignKey("users.user_id"))

    owner = relationship("User", back_populates="achievements")

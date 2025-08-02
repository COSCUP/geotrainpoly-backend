from sqlalchemy import Column, Integer, Text, Enum, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import engine, Base
from app.models.achievements import Achievement


class UserAchievement(Base):
    __tablename__ = "user_achievements"
    id = Column(Integer, autoincrement=True, primary_key=True)
    achievement_id = Column(Integer, ForeignKey("achievements.achievement_id"), primary_key=True)
    user_id = Column(String(40), ForeignKey("users.user_id"), primary_key=True)

    owner = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")

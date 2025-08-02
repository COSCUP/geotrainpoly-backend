from sqlalchemy import Column, Integer, Text, Enum, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import engine, Base


class Achievement(Base):
    __tablename__ = "achievements"
    achievement_id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text)
    points = Column(Integer)
    
    model = Column(String(30))
    column = Column(String(30))
    goal = Column(String(40), server_default="0")
    type = Column(String(30))

    user_achievements = relationship("UserAchievement", back_populates="achievement")

from sqlalchemy import Column, Integer, Text, Enum, String
from app.database import engine, Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(String(36), primary_key=True)
    name = Column(Text)
    avatar = Column(Text)
    title = Column(Text)
    points = Column(Integer, default=0)
    pass

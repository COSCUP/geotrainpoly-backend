from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Msg(Base):
    __tablename__ = "msg"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(String(40), ForeignKey("users.user_id"), primary_key=True)
    booth_id = Column(String(40), ForeignKey("booths.booth_id"), primary_key=True)
    content = Column(String(200))

    owner = relationship("User", back_populates="msg")
    booth = relationship("Booth", back_populates="msg")

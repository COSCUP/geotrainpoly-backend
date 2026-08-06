from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class UserBooths(Base):
    __tablename__ = "user_booths"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(String(40), ForeignKey("users.user_id"), primary_key=True)
    booth_id = Column(String(40), ForeignKey("booths.booth_id"), primary_key=True)
    x = Column(Integer, server_default="0")

    owner = relationship("User", back_populates="booths")
    booth = relationship("Booth", back_populates="users")

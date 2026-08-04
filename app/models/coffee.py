from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Coffee(Base):
    __tablename__ = "coffee"
    user_id = Column(String(40), ForeignKey("users.user_id"), primary_key=True)
    reward = Column(Boolean, server_default="0")
    
    owner = relationship("User", back_populates="coffee")

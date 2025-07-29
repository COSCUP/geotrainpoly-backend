from sqlalchemy import Column, Integer, Text, Enum, String
from sqlalchemy.orm import relationship
from app.database import engine, Base


class Booth(Base):
    __tablename__ = "booths"
    booth_id = Column(String(40), primary_key=True)
    name = Column(Text)
    description = Column(Text)
    logo = Column(Text)
    type = Column(Enum("BOOTHS", "ROOMS"))

    users = relationship("UserBooths", back_populates="booth")

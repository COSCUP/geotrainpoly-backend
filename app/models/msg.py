from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    TIMESTAMP,
    func,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.database import Base


class Msg(Base):
    __tablename__ = "msg"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(String(40), ForeignKey("users.user_id"), primary_key=True)
    booth_id = Column(String(40), ForeignKey("booths.booth_id"), primary_key=True)
    content = Column(String(200))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("user_id", "booth_id", name="uix_user_booth"),)
    owner = relationship("User", back_populates="msg")
    booth = relationship("Booth", back_populates="msg")

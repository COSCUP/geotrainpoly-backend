from sqlalchemy import Column, Integer, String, func
from sqlalchemy.dialects.mysql import TIMESTAMP
from app.database import Base


class Log(Base):
    __tablename__ = "log"
    log_id = Column(Integer, autoincrement=True, primary_key=True)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
    user_id = Column(String(40))
    booth_id = Column(String(40))
    action = Column(String(255))

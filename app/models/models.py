from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.database.database import Base

class RequestLog(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String)
    input = Column(String)
    result = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

from sqlalchemy import Column, String, DateTime
from datetime import datetime
from ..db.database import Base

class Session(Base):
    __tablename__ = "sessions"
    
    session_id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


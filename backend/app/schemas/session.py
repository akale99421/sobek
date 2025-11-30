from pydantic import BaseModel
from datetime import datetime

class SessionCreate(BaseModel):
    session_id: str

class SessionResponse(BaseModel):
    session_id: str
    created_at: datetime
    last_active: datetime
    
    class Config:
        from_attributes = True


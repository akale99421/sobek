from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy.orm import Session
from .core.config import settings
from .db.database import engine, get_db, Base
from .models.session import Session as SessionModel
from .schemas.session import SessionCreate, SessionResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Platinum Sequence API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "platinum-sequence-api"
    }

@app.post("/api/session", response_model=SessionResponse)
async def create_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    existing_session = db.query(SessionModel).filter(SessionModel.session_id == session_data.session_id).first()
    
    if existing_session:
        existing_session.last_active = datetime.utcnow()
        db.commit()
        db.refresh(existing_session)
        return existing_session
    
    new_session = SessionModel(session_id=session_data.session_id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

@app.get("/api/session/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


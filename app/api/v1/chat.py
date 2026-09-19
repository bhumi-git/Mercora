from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import ChatRequest
from app.services.chat import ask

router = APIRouter()

@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    answer = ask(db, request.question)
    return {"answer": answer}
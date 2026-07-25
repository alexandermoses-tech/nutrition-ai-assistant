from contextlib import asynccontextmanager
from datetime import datetime
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from gemini_service import generate_answer
from models import NutritionQuery


@asynccontextmanager
async def lifespan(app: FastAPI) -> Generator[None, None, None]:
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Nutrition AI Assistant",
    lifespan=lifespan,
)


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime


@app.get("/")
def health_check() -> dict[str, str]:
    return {
        "status": "Nutrition AI Assistant is running",
    }


@app.post("/ask", response_model=QuestionResponse)
def ask_gemini(
    request: QuestionRequest,
    db: Session = Depends(get_db),
) -> NutritionQuery:
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        answer = generate_answer(question)
    except Exception as error:
        print(f"Gemini API error: {error}")

        raise HTTPException(
            status_code=502,
            detail="Failed to get a response from Gemini.",
        ) from error

    try:
        query_record = NutritionQuery(
            question=question,
            answer=answer,
        )

        db.add(query_record)
        db.commit()
        db.refresh(query_record)

        return query_record

    except Exception as error:
        db.rollback()
        print(f"Database error: {error}")

        raise HTTPException(
            status_code=500,
            detail="The answer was generated but could not be saved.",
        ) from error
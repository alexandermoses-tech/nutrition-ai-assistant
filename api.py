from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from gemini_service import generate_answer


app = FastAPI(title="Nutrition AI Assistant")


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "Nutrition AI Assistant is running"}


@app.post("/ask")
def ask_gemini(request: QuestionRequest) -> dict[str, str]:
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        answer = generate_answer(question)

        return {
            "question": question,
            "answer": answer,
        }

    except Exception as error:
        print(f"Gemini API error: {error}")

        raise HTTPException(
            status_code=502,
            detail="Failed to get a response from Gemini.",
        ) from error
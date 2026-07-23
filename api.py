from fastapi import FastAPI, HTTPException
from google import genai
from pydantic import BaseModel


app = FastAPI(title="Nutrition AI Assistant")
client = genai.Client()


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
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=question,
        )

        return {
            "question": question,
            "answer": response.text or "",
        }

    except Exception as error:
        print(f"Gemini API error: {error}")

        raise HTTPException(
            status_code=502,
            detail="Failed to get a response from Gemini.",
        ) from error
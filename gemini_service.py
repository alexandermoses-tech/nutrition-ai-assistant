from google import genai

MODEL_NAME = "gemini-3.1-flash-lite"

client = genai.Client()


def generate_answer(question: str) -> str:
    """Send a question to Gemini and return the generated text."""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=question,
    )

    return response.text or ""
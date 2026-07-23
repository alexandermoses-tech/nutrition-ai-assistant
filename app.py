from google import genai


def ask_gemini(question: str) -> str:
    """Send a question to Gemini and return its response."""
    client = genai.Client()

    response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=question,
)

    return response.text


def main() -> None:
    question = input("Ask a nutrition question: ").strip()

    if not question:
        print("Question cannot be empty.")
        return

    try:
        answer = ask_gemini(question)
        print("\nGemini response:")
        print(answer)
    except Exception as error:
        print(f"\nRequest failed: {error}")


if __name__ == "__main__":
    main()
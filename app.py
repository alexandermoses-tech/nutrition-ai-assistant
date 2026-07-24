from gemini_service import generate_answer


def main() -> None:
    question = input("Ask a nutrition question: ").strip()

    if not question:
        print("Question cannot be empty.")
        return

    try:
        answer = generate_answer(question)

        print("\nGemini response:")
        print(answer)

    except Exception as error:
        print(f"\nRequest failed: {error}")


if __name__ == "__main__":
    main()
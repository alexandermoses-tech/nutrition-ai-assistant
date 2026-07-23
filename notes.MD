# What I Learned Today

- genai.Client() connects the Python program to Gemini API.
- API key authenticates the request.
- QuestionRequest validates incoming JSON.
- POST /ask sends the question to Gemini.
- 400 means invalid user input.
- 502 means FastAPI received the request, but Gemini failed.

# Next Step

Connect FastAPI to PostgreSQL and store:
- question
- answer
- created_at
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI(title="Voice Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # safe for Netlify + Render
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Voice Assistant API is running!"}

@app.post("/ask")
async def ask_ai(request: AskRequest):
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        return {"error": "PERPLEXITY_API_KEY not set"}

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.perplexity.ai"
    )

    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": request.text}
        ]
    )

    return {"reply": response.choices[0].message.content}

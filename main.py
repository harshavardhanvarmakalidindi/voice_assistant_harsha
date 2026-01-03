from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Voice Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:5500",
        "https://harshaprojecttest3.netlify.app",  # Your current frontend
        "https://gilded-custard-8db3f1.netlify.app"
    ],
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
    try:
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            return {"error": "PERPLEXITY_API_KEY not set"}

        client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant."},
                {"role": "user", "content": request.text}
            ]
        )
        return {"reply": response.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}
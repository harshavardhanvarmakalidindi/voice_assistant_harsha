from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -----------------------------
# App Initialization
# -----------------------------
app = FastAPI(
    title="Voice Assistant API",
    version="1.0.0"
)

# -----------------------------
# CORS Configuration
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:5500",
        "https://harshaprojecttest3.netlify.app",
        "https://gilded-custard-8db3f1.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Request Schema
# -----------------------------
class AskRequest(BaseModel):
    text: str

# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def root():
    return {"message": "Voice Assistant API is running!"}

# -----------------------------
# Ask AI Endpoint
# -----------------------------
@app.post("/ask")
async def ask_ai(request: AskRequest):
    user_text = request.text.lower().strip()

    # 🛑 Stop / Exit Commands
    stop_words = ["stop", "exit", "quit", "bye", "goodbye"]
    if user_text in stop_words:
        return {
            "reply": "Okay, stopping the assistant. Goodbye 👋",
            "end": True
        }

    try:
        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            return {"error": "PERPLEXITY_API_KEY not set"}

        # Create client per request (important for Render)
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.perplexity.ai"
        )

        response = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant."},
                {"role": "user", "content": request.text}
            ]
        )

        raw_reply = response.choices[0].message.content

        # ✅ Remove citation numbers like [1][2][4]
        clean_reply = re.sub(r"\[\d+\]", "", raw_reply).strip()

        return {
            "reply": clean_reply,
            "end": False
        }

    except Exception as e:
        return {"error": str(e)}

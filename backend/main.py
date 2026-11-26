import httpx
from fastapi import FastAPI
from pydantic import BaseModel

# Create the application
app = FastAPI(title="PA-Agent")

# First endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to your PA-Agent!",
        "status": "online"
    }

# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

# Define the structure of a chat message
class ChatRequest(BaseModel):
    message: str


# Chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):        
    user_message =request.message

    async with httpx.AsyncClient(timeout=300.0) as client:
        payload = {
            "model": "qwen2:7b",
            "messages": [
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            "stream": False 
        }
        response = await client.post(
        "http://localhost:11434/api/chat",
            json=payload
    )
        response.raise_for_status()  # Raise an error for bad responses

    data = response.json()
        
    return {
        "user_message": user_message,
        "response": data["message"]["content"],
        "status": "success"
    }

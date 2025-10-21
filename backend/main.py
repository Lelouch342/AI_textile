from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Allow CORS for frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

def query_hf(prompt: str):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt, "options": {"wait_for_model": True}}  # Ensures waiting for model to load

    response = requests.post(HF_MODEL_URL, headers=headers, json=payload)

    if response.status_code != 200:
        # Gracefully handle model loading or other errors
        if "loading" in response.text.lower():
            raise HTTPException(status_code=503, detail="Model is loading, please try again shortly.")
        raise HTTPException(status_code=response.status_code, detail=response.text)

    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        data = response.json()
        # Handle JSON response with base64 encoded image
        if isinstance(data, list) and "generated_image" in data[0]:
            return base64.b64decode(data[0]["generated_image"])
        raise HTTPException(status_code=422, detail="Unexpected JSON response format from model.")
    else:
        # Otherwise treat as raw image bytes
        return response.content

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate_image(req: PromptRequest):
    image_bytes = query_hf(req.prompt)
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return {"image": encoded, "message": "Image generated successfully"}

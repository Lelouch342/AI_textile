import os
import base64
import requests
import torch
import open_clip
import chromadb
from dotenv import load_dotenv
from fastapi import HTTPException

# Load environment variables
load_dotenv()

# --- Hugging Face API Setup ---
HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

def generate_image_service(prompt: str):
    """
    Calls Hugging Face API to generate an image from text.
    """
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt, "options": {"wait_for_model": True}}

    response = requests.post(HF_MODEL_URL, headers=headers, json=payload)

    if response.status_code != 200:
        if "loading" in response.text.lower():
            raise HTTPException(status_code=503, detail="Model is loading, please try again shortly.")
        raise HTTPException(status_code=response.status_code, detail=response.text)

    # Handle different response types
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        data = response.json()
        if isinstance(data, list) and "generated_image" in data[0]:
            return base64.b64decode(data[0]["generated_image"])
        raise HTTPException(status_code=422, detail="Unexpected JSON response format from model.")
    else:
        return response.content


# --- Chroma + CLIP Setup for Retrieval ---
CHROMA_PATH = "textile_db"
COLLECTION_NAME = "textile_images"
MODEL_NAME = "ViT-B-32"
PRETRAINED = "laion2B-s34B-b79K"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(COLLECTION_NAME)

device = "cuda" if torch.cuda.is_available() else "cpu"
model, _, preprocess = open_clip.create_model_and_transforms(MODEL_NAME, pretrained=PRETRAINED)
model = model.to(device)
model.eval()

def retrieve_images_service(query: str):
    """
    Retrieves most similar images from ChromaDB given a text query.
    """
    tokens = open_clip.tokenize([query]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(tokens)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    embedding = text_features.cpu().to(torch.float32).numpy()

    results = collection.query(query_embeddings=embedding.tolist(), n_results=5)

    output = []
    for id_, meta in zip(results["ids"][0], results["metadatas"][0]):
        output.append({
            "id": id_,
            "craft": meta.get("craft", "unknown"),
            "path": meta.get("path", ""),
        })
    return {"results": output}

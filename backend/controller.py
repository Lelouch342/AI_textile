from fastapi import APIRouter, Query
from pydantic import BaseModel
from services import retrieve_images_service, generate_image_service
import base64

router = APIRouter()

# ----- Image Retrieval -----
@router.get("/retrieve")
async def retrieve_images(query: str = Query(..., description="Text query")):
    return retrieve_images_service(query)


# ----- Image Generation -----
class PromptRequest(BaseModel):
    prompt: str

@router.post("/generate")
async def generate_image(req: PromptRequest):
    image_bytes = generate_image_service(req.prompt)
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return {"image": encoded, "message": "Image generated successfully"}

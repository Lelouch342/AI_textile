import os
import torch
from PIL import Image
import open_clip
import chromadb
import numpy as np

# --- Initialize Chroma ---
client = chromadb.PersistentClient(path="textile_db")
collection = client.get_or_create_collection(name="textile_images")

# --- Load CLIP model ---
print("📦 Loading OpenCLIP model...")
model, _, preprocess = open_clip.create_model_and_transforms(
    'ViT-B-32', pretrained='laion2B-s34B-b79K'
)
model.eval()
print("✅ Model loaded.")

# --- Prepare data ---
base_dir = "textile_data"
ids, metas, embeddings = [], [], []

for craft_folder in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, craft_folder)
    if not os.path.isdir(folder_path):
        continue

    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            file_path = os.path.join(folder_path, filename)
            try:
                image = preprocess(Image.open(file_path)).unsqueeze(0)

                # Compute embedding
                with torch.no_grad():
                    image_features = model.encode_image(image)
                    image_features /= image_features.norm(dim=-1, keepdim=True)
                    embedding = image_features.squeeze().cpu().numpy().tolist()

                ids.append(f"{craft_folder}_{filename}")
                metas.append({"craft": craft_folder, "path": file_path})
                embeddings.append(embedding)

            except Exception as e:
                print(f"⚠️ Skipping {file_path}: {e}")

# --- Add to Chroma ---
if embeddings:
    collection.add(ids=ids, embeddings=embeddings, metadatas=metas)
    print(f"✅ Added {len(embeddings)} image embeddings for Gond, Kalamkari, and Kasuti.")
else:
    print("❌ No embeddings generated. Check your image folders.")

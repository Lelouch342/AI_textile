import chromadb
import torch
import open_clip
from PIL import Image
import numpy as np

# --- Connect to your existing ChromaDB ---
client = chromadb.PersistentClient(path="textile_db")
collection = client.get_collection("textile_images")

# --- Load the same OpenCLIP model used before ---
model, _, preprocess = open_clip.create_model_and_transforms(
    'ViT-B-32', pretrained='laion2B-s34B-b79K'
)
tokenizer = open_clip.get_tokenizer('ViT-B-32')

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# --- Step 1: Pick a query image ---
query_path = "textile_data/gond/Download (41).jpeg"   # 👈 replace with your test image

image = Image.open(query_path).convert("RGB")
image_tensor = preprocess(image).unsqueeze(0).to(device)

# --- Step 2: Embed it ---
with torch.no_grad(), torch.amp.autocast(device_type=device):
    query_embedding = model.encode_image(image_tensor)

query_embedding = query_embedding / query_embedding.norm(dim=-1, keepdim=True)
embedding_np = query_embedding.cpu().to(torch.float32).numpy()

# --- Step 3: Query the database ---
results = collection.query(
    query_embeddings=embedding_np.tolist(),
    n_results=5  # top 5 most similar images
)

# --- Step 4: Print results ---
print("\n🔍 Top similar results:")
for i, meta in enumerate(results["metadatas"][0]):
    print(f"{i+1}. Craft: {meta['craft']}")
    print(f"   ID: {results['ids'][0][i]}")

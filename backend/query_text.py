# query_text.py
import chromadb
import open_clip
import torch
from PIL import Image
import numpy as np

# --- Config ---
CHROMA_PATH = "textile_db"        # same persistent path you used
COLLECTION_NAME = "textile_images"  # collection created earlier
MODEL_NAME = "ViT-B-32"
PRETRAINED = "laion2B-s34B-b79K"
N_RESULTS = 5

# --- Connect to Chroma ---
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection(COLLECTION_NAME)

# --- Load CLIP model (same one used for images) ---
device = "cuda" if torch.cuda.is_available() else "cpu"
print("device:", device)
model, _, preprocess = open_clip.create_model_and_transforms(MODEL_NAME, pretrained=PRETRAINED)
model = model.to(device)
model.eval()

# --- Prepare the query text ---
query_text = "peacock motifs in Kalamkari style"  # change this to experiment
print("Query:", query_text)

# Tokenize and get text embedding
# open_clip provides a helper `tokenize` which returns token IDs
tokens = open_clip.tokenize([query_text]).to(device)  # shape [1, seq_len]
with torch.no_grad():
    text_features = model.encode_text(tokens)         # tensor [1, d]
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)

# Convert to float32 numpy
embedding_np = text_features.cpu().to(torch.float32).numpy()

# --- Query Chroma using the embedding ---
results = collection.query(
    query_embeddings=embedding_np.tolist(),
    n_results=N_RESULTS
)

# --- Print results ---
print("\nTop matches:")
ids = results.get("ids", [[]])[0]
metas = results.get("metadatas", [[]])[0]

for i, (id_, meta) in enumerate(zip(ids, metas), start=1):
    craft = meta.get("craft", "unknown")
    path = meta.get("path", meta.get("file", "no-path"))
    print(f"{i}. Craft: {craft}")
    print(f"   ID: {id_}")
    print(f"   Path: {path}")

import chromadb
from chromadb.utils import embedding_functions
import os

# Initialize Chroma client
client = chromadb.PersistentClient(path="textile_db")

# Create embedding function for semantic similarity
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create or get collection with embeddings
collection = client.get_or_create_collection(
    name="textiles",
    embedding_function=embedding_function
)

# 🧹 Proper cleanup (avoid ValueError for empty filter)
try:
    all_items = collection.get()
    if all_items and "ids" in all_items and len(all_items["ids"]) > 0:
        collection.delete(ids=all_items["ids"])
        print(f"🧹 Cleared {len(all_items['ids'])} old records.")
except Exception as e:
    print("⚠️ Skipping cleanup:", e)

# 📂 Load your craft descriptions
data_dir = "textile_data"
texts, ids, metadatas = [], [], []

for i, filename in enumerate(os.listdir(data_dir)):
    if filename.endswith(".txt"):
        with open(os.path.join(data_dir, filename), "r", encoding="utf-8") as f:
            text = f.read().strip()
            texts.append(text)
            ids.append(str(i))
            metadatas.append({"filename": filename})

# ➕ Add data to collection
collection.add(documents=texts, ids=ids, metadatas=metadatas)

print(f"✅ Loaded {len(texts)} craft descriptions into ChromaDB.")

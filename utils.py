from google import genai
import os
import faiss
from sentence_transformers import SentenceTransformer
import json
import numpy as np

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gc_client = genai.Client(api_key=GOOGLE_API_KEY)


def load_model_and_fiass_index():
    sentence_transformer_model = SentenceTransformer("all-MiniLM-L6-v2")
    faiss_index = faiss.read_index("embeddings.index")

    return sentence_transformer_model, faiss_index


def sync_embeddings(products):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    corpus = [f"{p['product_name']} {p['description']} " for p in products]
    embeddings = model.encode(corpus).astype("float32")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, "embeddings.index")

    np.save("embeddings.npy", embeddings)
    with open("products.json", "w") as f:
        json.dump(products, f, indent=4)

    return True
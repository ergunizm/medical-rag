import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

PROCESSED_DATA_PATH = "../data/processed/processed_chunks.json"
VECTOR_STORE_PATH = "../data/vector/"
INDEX_FILE = os.path.join(VECTOR_STORE_PATH, "faiss_index.bin")
METADATA_FILE = os.path.join(VECTOR_STORE_PATH, "metadata.json")
EMBEDDING_MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2' 

with open(PROCESSED_DATA_PATH, 'r', encoding='utf-8') as f:
    chunks = json.load(f)

model = SentenceTransformer(EMBEDDING_MODEL_NAME, device='cpu') 

texts = [chunk['text'] for chunk in chunks]

embeddings = model.encode(texts, show_progress_bar=True)

embedding_dim = embeddings.shape[1]

index = faiss.IndexFlatL2(embedding_dim)
index.add(np.array(embeddings).astype('float32'))

os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
faiss.write_index(index, INDEX_FILE)

metadata = {i: chunk for i, chunk in enumerate(chunks)}
with open(METADATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, ensure_ascii=False, indent=4)
    
print("Vektör veritabanı oluşturuldu!")

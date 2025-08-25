import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

EMBEDDING_MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
LLM_MODEL_NAME = "google/flan-t5-base"

VECTOR_STORE_PATH = os.path.join(BASE_DIR, "data/vector")
INDEX_FILE = os.path.join(VECTOR_STORE_PATH, "faiss_index.bin")
METADATA_FILE = os.path.join(VECTOR_STORE_PATH, "metadata.json")
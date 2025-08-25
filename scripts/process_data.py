import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import fitz

SOURCE_DATA_PATH = "../data/raw"
PROCESSED_DATA_PATH = "../data/processed/processed_chunks.json"

def read_document_content(filepath):
    doc = fitz.open(filepath)
    content = ""
    for page in doc:
        content += page.get_text()
    return content


def process_documents():
    documents = []
    for filename in os.listdir(SOURCE_DATA_PATH):
        filepath = os.path.join(SOURCE_DATA_PATH, filename)
        content = read_document_content(filepath)
        if content:
            documents.append({"content": content, "source": filename})

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )

    processed_chunks = []
    for doc in documents:
        chunks = text_splitter.split_text(doc["content"])
        for i, chunk_text in enumerate(chunks):
            processed_chunks.append({
                "text": chunk_text,
                "metadata": {"source": doc["source"], "chunk_id": i}
            })
    
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    
    with open(PROCESSED_DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(processed_chunks, f, ensure_ascii=False, indent=4)
        
    print(f"Veri işlendi ve {len(processed_chunks)} chunk {PROCESSED_DATA_PATH} dosyasına kaydedildi.")

process_documents()
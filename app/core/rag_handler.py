import time
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from .config import INDEX_FILE, METADATA_FILE, EMBEDDING_MODEL_NAME, LLM_MODEL_NAME

class MedicalRAG:
    def __init__(self):
        self.embedding_model = None
        self.llm_pipeline = None
        self.index = None
        self.metadata = None
        self.load_models()

    def load_models(self):
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME, device='cpu')
        self.index = faiss.read_index(INDEX_FILE)
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            raw_metadata = json.load(f)
            self.metadata = {int(k): v for k, v in raw_metadata.items()}

        tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME)
        model = AutoModelForSeq2SeqLM.from_pretrained(LLM_MODEL_NAME)
        self.llm_pipeline = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=512,
            truncation=True
        )
        print("Tüm modeller başarıyla yüklendi.")

    def retrieve(self, query: str, k: int = 3):
        start_time = time.time()
        query_embedding = self.embedding_model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)
        
        retrieved_docs = [self.metadata[idx] for idx in indices[0]]
        
        end_time = time.time()
        retrieval_time_ms = (end_time - start_time) * 1000
        return retrieved_docs, retrieval_time_ms

    def generate(self, query: str, context_docs: list):
        start_time = time.time()
        
        context = "\n\n".join([doc['text'] for doc in context_docs])
        
        prompt = f"""
        Answer the given question using the following context information.
        If the answer is not in the context, say 'I dont have this information'


        Context:
        {context}

        Question: {query}

        Answer:
        """
        
        result = self.llm_pipeline(prompt)
        answer = result[0]['generated_text']

        end_time = time.time()
        generation_time_ms = (end_time - start_time) * 1000
        return answer, generation_time_ms

    def process_query(self, query: str):
        retrieved_docs, retrieval_time = self.retrieve(query)
        answer, generation_time = self.generate(query, retrieved_docs)
        
        total_time = retrieval_time + generation_time
        
        sources = [{"text": doc["text"], "source": doc["metadata"]["source"]} for doc in retrieved_docs]
        
        return {
            "answer": answer,
            "sources": sources,
            "latency_ms": {
                "retrieval": round(retrieval_time),
                "generation": round(generation_time),
                "total": round(total_time)
            }
        }
    
rag_system = MedicalRAG()
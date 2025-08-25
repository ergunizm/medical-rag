from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from app.core.rag_handler import rag_system
import os
from pathlib import Path

class QueryRequest(BaseModel):
    question: str

app = FastAPI(
    title="Medical RAG",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.post("/api/query")
async def process_query_endpoint(request: QueryRequest):
    result = rag_system.process_query(request.question)
    return result

@app.get("/api/", summary="Health Check")
def read_root():
    return {"status": "ok", "message": "Medical RAG API is running."}

APP_DIR = os.path.dirname(__file__)
BUILD_DIR = os.path.abspath(os.path.join(APP_DIR, "..", "react-front", "build"))
app.mount("/", StaticFiles(directory=BUILD_DIR, html=True), name="static")

@app.get("/", summary="Serve React Frontend")
async def serve_react_app():
    build_path = Path(BUILD_DIR)
    
    index_path = build_path / "index.html"
    if not index_path.is_file():
        return JSONResponse(
            status_code=404,
            content={"error": "Frontend build files not found. Make sure the React app is built."}
        )
    return FileResponse(str(index_path))
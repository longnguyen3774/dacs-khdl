# Server FastAPI tìm kiếm sách theo review khách hàng, fallback nếu không có kết quả

import json
import re
import html
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# Load model encode query
model = SentenceTransformer('all-MiniLM-L6-v2')

# Kết nối Qdrant
qdrant_client = QdrantClient(host="localhost", port=6333)
collection_name = "reviews"

# Khởi tạo FastAPI
app = FastAPI()

# Tiền xử lý query nhập vào
def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'[^\w\s.,!?-]', ' ', text)
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Load danh sách fallback books
def get_fallback_books(top_k=5):
    with open('C:/Users/Nami/Desktop/DACS/top_books.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data["fallback_books"][:top_k]

# Định nghĩa request và response model
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    id: int
    name: str
    score: float

# API tìm kiếm sách
@app.post("/search", response_model=List[SearchResult])
def search_books(req: SearchRequest):
    query_vector = model.encode(clean_text(req.query)).tolist()
    results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=req.top_k
    )

    if results:
        return [
            SearchResult(id=hit.id, name=hit.payload.get("name", ""), score=hit.score)
            for hit in results
        ]
    else:
        fallback = get_fallback_books(req.top_k)
        return [
            SearchResult(id=book["id"], name=book["name"], score=0.0)
            for book in fallback
        ]

print("API Server Ready!")
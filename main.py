from fastapi import FastAPI
from pydantic import BaseModel
import chromadb

class Doc(BaseModel):
    id: str
    content: str

class Query(BaseModel):
    query: str

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="docs")

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ML Service is running"}

# This matches what your C# calls: /ingest
@app.post("/ingest")
def ingest(doc: Doc):
    collection.upsert(ids=[doc.id], documents=[doc.content])
    return {"ok": True, "id": doc.id}

# This matches what your C# calls: /documents (optional, for listing)
@app.get("/documents")
def list_docs():
    data = collection.get()
    return data

# Keep old ones too for direct testing
@app.post("/upsert")
def upsert(id: str, text: str):
    collection.upsert(ids=[id], documents=[text])
    return {"ok": True}

@app.post("/search")
def search(q: Query):
    return collection.query(query_texts=[q.query], n_results=3)

# This is what C# calls for search
@app.post("/query")
def query_rag(q: Query):
    return collection.query(query_texts=[q.query], n_results=3)
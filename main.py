import chromadb
from fastapi import FastAPI

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="docs")

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ML Service is running"}
@app.post("/upsert")
def upsert(id:str,text:str):
    collection.upsert(ids=[id],documents=[text])
    return {"ok": True}
@app.post("/search")
def search(query:str):
    return collection.query(query_texts=[query], n_results=3)
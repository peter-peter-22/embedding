from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel

app = FastAPI()
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dimensional embeddings

class EmbeddingInput(BaseModel):
    text: str

@app.post("/embed")
async def generate_embedding(body:EmbeddingInput):
    embedding = model.encode(body.text, convert_to_tensor=False).tolist()
    return {"embedding": embedding}
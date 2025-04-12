from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from fastapi import APIRouter
import asyncio

router = APIRouter()

model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dimensional embeddings

class EmbeddingInput(BaseModel):
    text: str

sem = asyncio.Semaphore(4)

@router.post("/embedding")
async def generate_embedding_route(body:EmbeddingInput):
    async with sem:
        embedding = await asyncio.to_thread(generate_embedding,body.text)
        return {"embedding": embedding}

def generate_embedding(text):
    return model.encode(text, convert_to_tensor=False).tolist()
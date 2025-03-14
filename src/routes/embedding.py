from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from diskcache import Cache
from fastapi import APIRouter

router = APIRouter()

model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dimensional embeddings
cache = Cache(".cache")

class EmbeddingInput(BaseModel):
    text: str

@router.post("/embedding")
async def generate_embedding(body:EmbeddingInput):
    embedding = generate_embedding(body.text)
    return {"embedding": embedding}

#cache is useful because the generated posts are often repeated
@cache.memoize()
def generate_embedding(text):
    return model.encode(text, convert_to_tensor=False).tolist()
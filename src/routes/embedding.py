from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dimensional embeddings

class EmbeddingInput(BaseModel):
    text: str

@router.post("/embedding")
def generate_embedding_route(body:EmbeddingInput):
    embedding = generate_embedding(body.text)
    return {"embedding": embedding}
    

def generate_embedding(text):
    return model.encode(text, convert_to_tensor=False).tolist()
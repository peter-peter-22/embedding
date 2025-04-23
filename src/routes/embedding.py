from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from fastapi import APIRouter
import torch
from typing import List
router = APIRouter()

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model = SentenceTransformer('all-MiniLM-L6-v2',device=device)  # 384-dimensional embeddings

class EmbeddingInput(BaseModel):
    texts: List[str]

@router.post("/embedding")
def generate_embedding_route(body:EmbeddingInput):
    embeddings = generate_embeddings(body.texts)
    return {"embeddings": embeddings}

def generate_embeddings(text):
    return model.encode(text, convert_to_tensor=False).tolist()
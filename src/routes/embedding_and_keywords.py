from pydantic import BaseModel
from fastapi import APIRouter
from typing import List
from src.common.generate_embeddings import generate_embeddings
from src.common.extract_keywords import extract_keywords

router = APIRouter()

class EmbeddingInput(BaseModel):
    texts: List[str]

@router.post("/embedding")
def generate_embedding_route(body:EmbeddingInput):
    # Get embedding vectors
    embeddings = generate_embeddings(body.texts)
    # Get keywords
    keywords = extract_keywords(body.texts, embeddings)
    return {"embeddings": embeddings, "keywords": keywords}
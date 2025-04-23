from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from fastapi import APIRouter
import torch

router = APIRouter()

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model = SentenceTransformer('all-MiniLM-L6-v2',device=device)  # 384-dimensional embeddings

class EmbeddingInput(BaseModel):
    text: str

@router.post("/embedding")
def generate_embedding_route(body:EmbeddingInput):
    # TODO: 10k empty requests take 13s to process, while 10k embeddings take 7s on GPU, or 33s on CPU (1 thread). Creating the batches on the nodejs server would solve this.
    embedding = generate_embedding(body.text)
    return {"embedding": embedding}

def generate_embedding(text):
    return model.encode(text, convert_to_tensor=False).tolist()
from sentence_transformers import SentenceTransformer
import torch
from typing import List

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SentenceTransformer('all-MiniLM-L6-v2',device=device)  # 384-dimensional embeddings

type Vector=List[float]

def generate_embeddings(text)->List[Vector]:
    """Generate embedding vectors for texts"""
    return model.encode(text, convert_to_tensor=False).tolist()
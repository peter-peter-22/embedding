import torch
from fastapi import APIRouter
import time
from sentence_transformers import SentenceTransformer

router = APIRouter()

@router.get("/batch_test")
def batch_test():
    if not torch.cuda.is_available():
        raise Exception("GPU unavailable.")

    print("Generating",flush=True)
    sentences=["Sports bring people together like nothing else. Whether you're playing or cheering, it's all about the passion."]*10000

    model_gpu = SentenceTransformer('all-MiniLM-L6-v2',device="cuda")

    print("Processing",flush=True)
    sizes=[4096,2048,1024,512,256,128,64,32,16]
    for size in sizes:
        start = time.time()
        model_gpu.encode(sentences, batch_size=size, device="cuda").tolist()
        print(f"Size: {size}, Time: {time.time() - start:.1f}",flush=True)


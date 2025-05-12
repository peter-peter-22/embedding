import torch
from fastapi import APIRouter
import time
from sentence_transformers import SentenceTransformer
from concurrent.futures import ThreadPoolExecutor
import numpy as np

router = APIRouter()

@router.get("/stress_test")
def stress_test():
    if not torch.cuda.is_available():
        raise Exception("GPU unavailable.")

    print("Generating",flush=True)
    sentences=["Sports bring people together like nothing else. Whether you're playing or cheering, it's all about the passion."]*10000

    chunk_size = 100  
    chunks = [sentences[i:i + chunk_size] for i in range(0, len(sentences), chunk_size)]

    model_cpu = SentenceTransformer('all-MiniLM-L6-v2',device="cpu")
    model_gpu = SentenceTransformer('all-MiniLM-L6-v2',device="cuda")
    model_gpu.encode("warm up")

    print("Processing CPU",flush=True)
    start = time.time()
    model_cpu.encode(sentences).tolist()
    print("CPU Time:", time.time() - start,flush=True)

    print("Processing CPU threadpool",flush=True)
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        embeddings = list(executor.map(model_cpu.encode, chunks))
    embeddings = np.vstack(embeddings)
    print("CPU threadpool time:", time.time() - start,flush=True)

    print("Processing GPU",flush=True)
    start = time.time()
    model_gpu.encode(sentences, batch_size=128).tolist()
    print("GPU Time:", time.time() - start,flush=True)

    print("Processing GPU multi",flush=True)
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        embeddings = list(executor.map(lambda texts: model_gpu.encode(texts,batch_size=128), chunks))
    embeddings = np.vstack(embeddings)
    print("GPU multi time:", time.time() - start,flush=True)

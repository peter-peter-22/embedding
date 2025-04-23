# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from src.routes.embedding import router as embedding_router
from src.routes.home import router as home_router
from src.routes.graph_clustering import router as clustering_router
from src.routes.visualize_clusters import router as visualize_clusters_router
from src.routes.stress_test import router as stress_test_router
from src.routes.batch_size_test import router as batch_test

app = FastAPI()

# routers
app.include_router(embedding_router)
app.include_router(home_router)
app.include_router(clustering_router)
app.include_router(visualize_clusters_router)
app.include_router(stress_test_router)
app.include_router(batch_test)
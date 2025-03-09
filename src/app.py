from fastapi import FastAPI
from src.routes.embedding import router as embedding_router
from src.routes.home import router as home_router
from src.routes.clustering import router as clustering_router

app = FastAPI()

# routers
app.include_router(embedding_router)
app.include_router(home_router)
app.include_router(clustering_router)
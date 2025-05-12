from fastapi import FastAPI
from src.routes.embedding_and_keywords import router as embedding_router
from src.routes.home import router as home_router
from src.routes.stress_test import router as stress_test_router
from src.routes.batch_size_test import router as batch_test

app = FastAPI()

# routers
app.include_router(embedding_router)
app.include_router(home_router)
app.include_router(stress_test_router)
app.include_router(batch_test)
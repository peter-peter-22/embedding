from fastapi import APIRouter

router = APIRouter(prefix="/embedding")

# home page to check if the server works
@router.get("/")
def home():
    return "Hello from Python!"
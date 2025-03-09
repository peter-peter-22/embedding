from fastapi import APIRouter

router = APIRouter(prefix="/clustering")

# home page to check if the server works
@router.get("/")
def home():
    return "Hello from clustering!"
from fastapi import APIRouter
from src.db import db

router = APIRouter(prefix="/clustering")

# Home page to check if the server works
@router.get("/")
def generateClusters():
     with db.cursor() as cursor:
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("Database version:", db_version)
        return "Hello from clustering!"
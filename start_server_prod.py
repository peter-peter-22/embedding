import uvicorn

def main():
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=False, workers=4)
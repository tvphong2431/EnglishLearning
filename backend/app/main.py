from fastapi import FastAPI
from app.api.process import router as process_router

app = FastAPI()
app.include_router(process_router)

@app.get("/")
def root():
    return {
        "message": "EnglishLearning API is running"
    }
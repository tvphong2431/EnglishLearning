from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.errors import AppError
from app.api.process import router as process_router


app = FastAPI()
app.include_router(process_router)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code" : exc.code,
            "message" : exc.message,
        },
    )

@app.get("/")
def root():
    return {
        "message": "EnglishLearning API is running"
    }

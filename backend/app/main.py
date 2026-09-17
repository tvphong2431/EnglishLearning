from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.session import router as session_router
from app.errors import AppError


app = FastAPI()
app.include_router(session_router)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.message,
        },
    )


@app.get("/")
def root():
    return {
        "message": "EnglishLearning API is running"
    }
from fastapi import FastAPI

from app.api.upload import router as upload_router
from app.api.analysis import router as analysis_router
from app.api import chat

app = FastAPI(
    title="FinSight AI",
    version="1.0.0"
)

app.include_router(upload_router)
app.include_router(analysis_router)
app.include_router(chat.router)

@app.get("/")
def home():
    return {
        "message": "Welcome to FinSight AI"
    }
    
    
    
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.analysis import router as analysis_router
from app.api.report import router as report_router
from app.api import chat
from app.api import statements

app = FastAPI(
    title="FinSight AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
                    "http://localhost:5173",
                    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(analysis_router)
app.include_router(chat.router)
app.include_router(report_router)
app.include_router(statements.router)

@app.get("/")
def home():
    return {
        "message": "Welcome to FinSight AI"
    }
    
    
    
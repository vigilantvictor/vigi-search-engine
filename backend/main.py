from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import router
from app.database import initialize_database

app = FastAPI(
    title="Vigi Personal AI Search Engine",
    description="AI-powered personal web search engine",
    version="1.0.0"
)
initialize_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "name": "Vigi Personal AI Search Engine",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
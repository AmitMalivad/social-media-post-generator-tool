from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import content
from app.core.database import init_db

app = FastAPI(
    title="Social Content Generator API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(content.router, prefix="/api/v1/content", tags=["Content"])

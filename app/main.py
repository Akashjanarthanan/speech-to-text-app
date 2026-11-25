from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from .database import Base, engine
from . import models
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Speech to Text", version="1.0.0", description="Speech transcription and history CRUD MVP")
app.include_router(router)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

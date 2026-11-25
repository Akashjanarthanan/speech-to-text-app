from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path
import tempfile, os
from .database import get_db
from .models import Transcription
from .schemas import TranscriptionCreate, TranscriptionUpdate, TranscriptionOut
from .speech_service import transcribe_audio

router = APIRouter(prefix="/api", tags=["Transcriptions"])

@router.get("/transcriptions", response_model=list[TranscriptionOut])
def list_transcriptions(db: Session = Depends(get_db)):
    return db.query(Transcription).order_by(Transcription.created_at.desc()).all()

@router.get("/transcriptions/{item_id}", response_model=TranscriptionOut)
def get_transcription(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Transcription).filter(Transcription.id == item_id).first()
    if not item:
        raise HTTPException(404, "Transcription not found")
    return item

@router.post("/transcriptions", response_model=TranscriptionOut)
def create_transcription(payload: TranscriptionCreate, db: Session = Depends(get_db)):
    item = Transcription(title=payload.title, transcript=payload.transcript, language=payload.language)
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.put("/transcriptions/{item_id}", response_model=TranscriptionOut)
def update_transcription(item_id: int, payload: TranscriptionUpdate, db: Session = Depends(get_db)):
    item = db.query(Transcription).filter(Transcription.id == item_id).first()
    if not item:
        raise HTTPException(404, "Transcription not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit(); db.refresh(item)
    return item

@router.delete("/transcriptions/{item_id}")
def delete_transcription(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Transcription).filter(Transcription.id == item_id).first()
    if not item:
        raise HTTPException(404, "Transcription not found")
    db.delete(item); db.commit()
    return {"message": "Transcription deleted"}

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    suffix = Path(file.filename or "audio.webm").suffix or ".webm"
    if suffix.lower() not in {".webm", ".wav", ".mp3", ".m4a", ".ogg", ".mp4"}:
        raise HTTPException(400, "Unsupported audio file format")
    data = await file.read()
    if not data:
        raise HTTPException(400, "Empty audio file")
    if len(data) > 25 * 1024 * 1024:
        raise HTTPException(413, "Audio file exceeds 25 MB")
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data); temp_path = tmp.name
        text, language = transcribe_audio(temp_path)
        return {"transcript": text, "language": language}
    except Exception as exc:
        raise HTTPException(500, f"Transcription failed: {str(exc)}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

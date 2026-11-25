from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TranscriptionCreate(BaseModel):
    title: str = "Untitled transcription"
    transcript: str
    language: Optional[str] = None

class TranscriptionUpdate(BaseModel):
    title: Optional[str] = None
    transcript: Optional[str] = None
    language: Optional[str] = None

class TranscriptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    transcript: str
    language: Optional[str]
    created_at: datetime
    updated_at: datetime

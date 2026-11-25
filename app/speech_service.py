import os
from dotenv import load_dotenv
from faster_whisper import WhisperModel

load_dotenv()
_model = None

def get_model():
    global _model
    if _model is None:
        model_name = os.getenv("WHISPER_MODEL", "base")
        device = os.getenv("WHISPER_DEVICE", "cpu")
        compute_type = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
        _model = WhisperModel(model_name, device=device, compute_type=compute_type)
    return _model

def transcribe_audio(path: str):
    model = get_model()
    segments, info = model.transcribe(path, beam_size=3, vad_filter=True)
    text = " ".join(segment.text.strip() for segment in segments).strip()
    return text, info.language

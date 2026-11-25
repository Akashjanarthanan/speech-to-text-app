# Speech to Text — Real-Time Multilingual Transcription

Python FastAPI + MySQL + Faster-Whisper + browser audio capture. Includes transcription history CRUD.

## Features
- Microphone recording in the browser
- Audio upload transcription via Faster-Whisper (Hindi, English and other supported languages)
- Save, list, view, edit and delete transcription history
- MySQL database using SQLAlchemy
- Transcript download as plain text from the browser

> Note: this MVP records audio in the browser and submits it for transcription when recording is stopped. It is not word-by-word streaming transcription. This is a practical partial-assignment implementation. True streaming can be added with a streaming ASR server such as WhisperLiveKit.

## Setup (Windows)

1. Install Python 3.11, MySQL Server and (optionally) MySQL Workbench.
2. Create a database:
   ```sql
   CREATE DATABASE speech_to_text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Copy `.env.example` to `.env`, then update the MySQL password/URL.
4. In CMD, from this project folder:
   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
5. Run:
   ```bat
   uvicorn app.main:app --reload
   ```
6. Open http://127.0.0.1:8000

The first transcription may download the selected Whisper model and take longer.

## API
- `GET /api/transcriptions`
- `GET /api/transcriptions/{id}`
- `POST /api/transcriptions`
- `PUT /api/transcriptions/{id}`
- `DELETE /api/transcriptions/{id}`
- `POST /api/transcribe` — upload audio for recognition

## Model configuration
Set `WHISPER_MODEL` in `.env` to `tiny`, `base`, `small`, or `medium`. CPU mode is the default. Model performance depends on hardware.

## Assignment scope
This is an MVP demonstrating Python, FastAPI, relational database CRUD, browser microphone capture, and speech recognition. Recognition is performed after recording ends, not continuously as audio arrives.

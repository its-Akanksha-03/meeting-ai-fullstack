# 🎙️ Meeting Audio Intelligence (Full-Stack AI)

An end-to-end full-stack web application that transcribes spoken meeting recordings with timestamps and automatically generates structured executive summaries using Hugging Face Transformer models.

---

## 🏗️ Tech Stack
* **Frontend:** Angular 18 (Standalone Components, TypeScript, Reactive HTTP)
* **Backend:** FastAPI (Async REST API, CORS Middleware, Librosa Audio Processing)
* **Speech-to-Text (ASR):** Hugging Face `openai/whisper-tiny`
* **Summarization:** Hugging Face `sshleifer/distilbart-cnn-12-6`

---

## 🚀 Getting Started

### 1. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install soundfile librosa ffmpeg-python
python app.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```

Visit `http://localhost:4200` in your browser.

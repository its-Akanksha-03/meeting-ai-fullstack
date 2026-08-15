import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pipeline import MeetingProcessor

app = FastAPI(title="Meeting Audio Intelligence API")

# Allow Angular frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

processor = MeetingProcessor()
os.makedirs("temp_audio", exist_ok=True)

@app.post("/api/process-audio")
async def process_audio(file: UploadFile = File(...)):
    temp_path = f"temp_audio/{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        results = processor.process(temp_path)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
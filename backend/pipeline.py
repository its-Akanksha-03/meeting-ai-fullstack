import os
import torch
import librosa
from transformers import pipeline

class MeetingProcessor:
    def __init__(self):
        self.device = 0 if torch.cuda.is_available() else -1
        
        self.asr = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-tiny",
            chunk_length_s=30,
            device=self.device
        )
        self.summarizer = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",
            device=self.device
        )

    def process(self, audio_path: str):
        # Decode and load audio safely to 16kHz
        audio_array, sampling_rate = librosa.load(audio_path, sr=16000)
        
        audio_input = {
            "raw": audio_array,
            "sampling_rate": sampling_rate
        }

        # 1. Transcribe with timestamps
        asr_out = self.asr(
            audio_input, 
            return_timestamps=True, 
            generate_kwargs={"task": "transcribe"}
        )
        raw_text = asr_out.get("text", "").strip()

        chunks = asr_out.get("chunks", [])
        lines = []
        for chunk in chunks:
            ts = chunk.get("timestamp", (0.0, 0.0))
            start_sec = ts[0] if ts[0] is not None else 0.0
            end_sec = ts[1] if ts[1] is not None else 0.0
            
            start = f"{int(start_sec // 60):02d}:{int(start_sec % 60):02d}"
            end = f"{int(end_sec // 60):02d}:{int(end_sec % 60):02d}" if ts[1] else "..."
            lines.append(f"[{start} - {end}] {chunk.get('text', '')}")

        formatted_transcript = "\n".join(lines) if lines else raw_text

        # 2. Summarize
        if len(raw_text.split()) >= 15:
            summary_out = self.summarizer(raw_text, max_length=150, min_length=20, do_sample=False)
            summary_text = summary_out[0]["summary_text"]
        else:
            summary_text = raw_text if raw_text else "Transcript was too brief to generate a distinct summary."

        return {
            "raw_text": raw_text,
            "transcript": formatted_transcript,
            "summary": summary_text
        }
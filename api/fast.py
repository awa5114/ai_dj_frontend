from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from ai_dj import params
from google.cloud import storage
import soundfile
import io

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def index(filename):
    #?filename=1019315 Guido Sava - Fever (Original Mix).wav
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    blob = bucket.blob(f'data/audio_wav/{filename}')
    bts = blob.download_as_bytes()
    bts.seek
    return StreamingResponse(bts, media_type="audio/wav")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


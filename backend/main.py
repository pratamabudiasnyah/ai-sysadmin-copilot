from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="AI SysAdmin Copilot")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def root():
    with open("templates/index.html", "r") as f:
        return f.read()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload-log")
async def upload_log(file: UploadFile = File(...)):
    allowed_extensions = [".log", ".txt"]
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Hanya file .log dan .txt yang diperbolehkan.")
    content = await file.read()
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    return {"status": "success", "filename": filename, "size": len(content), "message": f"File {filename} berhasil diupload"}

@app.post("/analyze-log")
async def analyze_log(file: UploadFile = File(...)):
    allowed_extensions = [".log", ".txt"]
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Hanya file .log dan .txt yang diperbolehkan.")
    content = await file.read()
    log_text = content.decode("utf-8", errors="ignore")
    prompt = "Anda adalah asisten SysAdmin berpengalaman. Analisis log berikut dan berikan:\n1. RINGKASAN MASALAH\n2. PENJELASAN SEDERHANA\n3. REKOMENDASI SOLUSI\n\nLog:\n" + log_text
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return {"filename": filename, "analysis": response.text}

@app.get("/logs")
def list_logs():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files, "total": len(files)}

from fastapi import FastAPI, UploadFile, File, HTTPException
import os

app = FastAPI(title="AI SysAdmin Copilot")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "AI SysAdmin Copilot is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload-log")
async def upload_log(file: UploadFile = File(...)):
    # Validasi ekstensi file
    allowed_extensions = [".log", ".txt"]
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File tidak valid. Hanya .log dan .txt yang diperbolehkan."
        )
    
    # Simpan file
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {
        "status": "success",
        "filename": filename,
        "size": len(content),
        "message": f"File {filename} berhasil diupload"
    }

@app.get("/logs")
def list_logs():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files, "total": len(files)}

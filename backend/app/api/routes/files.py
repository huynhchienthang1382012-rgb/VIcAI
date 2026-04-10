from pathlib import Path
from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/files", tags=["files"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    out = UPLOAD_DIR / file.filename
    content = await file.read()
    out.write_bytes(content)
    return {"filename": file.filename, "size": len(content), "path": str(out)}

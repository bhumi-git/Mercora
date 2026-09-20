import shutil
import tempfile
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.ingestion import read_file, ingest_dataframe
from app.core.auth import verify_api_key

router = APIRouter()

@router.post("/datasets")
async def upload_dataset(file: UploadFile = File(...), db: Session = Depends(get_db), _: None = Depends(verify_api_key)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    df = read_file(tmp_path)
    result = ingest_dataframe(df, db)
    return result
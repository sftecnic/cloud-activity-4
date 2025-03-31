from fastapi import APIRouter, HTTPException, Header, UploadFile, File, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid

from files.domain.file import FileRecord, create_file, get_file, delete_file, list_files
from files.dependency_injection.di import s3_service
from authentication.dependency_injection.di import redis_service

router = APIRouter(prefix="/files", tags=["files"])

class FileCreateRequest(BaseModel):
    filename: str
    description: Optional[str] = None

class FileMergeRequest(BaseModel):
    file_ids: List[str]

def get_current_user(Auth: str = Header(...)):
    user_email = redis_service.get_user_id(Auth)
    if not user_email:
        raise HTTPException(status_code=401, detail="Token inválido")
    return user_email

@router.get("/")
def get_files(current_user: str = Depends(get_current_user)):
    files = list_files(current_user)
    return {"files": files}

@router.post("/")
def create_file_record(request: FileCreateRequest, current_user: str = Depends(get_current_user)):
    file_id = str(uuid.uuid4())
    file_record = FileRecord(id=file_id, filename=request.filename, description=request.description, owner=current_user)
    create_file(file_record)
    return {"file_id": file_id}

@router.post("/merge")
def merge_files(request: FileMergeRequest, current_user: str = Depends(get_current_user)):
    # Implementación dummy para fusión de PDFs
    merged_file_id = str(uuid.uuid4())
    file_record = FileRecord(
        id=merged_file_id,
        filename="merged.pdf",
        description="Archivo fusionado",
        owner=current_user
    )
    create_file(file_record)
    return {"merged_file_id": merged_file_id}

@router.get("/{file_id}")
def get_file_record(file_id: str, current_user: str = Depends(get_current_user)):
    file_record = get_file(file_id)
    if not file_record or file_record.owner != current_user:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    try:
        file_content = s3_service.download_file(file_id)
    except Exception:
        file_content = None
    return {
        "file": file_record,
        "content": file_content.decode("utf-8") if file_content else None
    }

@router.delete("/{file_id}")
def delete_file_record(file_id: str, current_user: str = Depends(get_current_user)):
    file_record = get_file(file_id)
    if not file_record or file_record.owner != current_user:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    delete_file(file_id)
    try:
        s3_service.delete_file(file_id)
    except Exception:
        pass
    return {"message": "Archivo eliminado correctamente"}

@router.post("/{file_id}")
def upload_file_content(
    file_id: str,
    current_user: str = Depends(get_current_user),
    file: UploadFile = File(...)
):
    file_record = get_file(file_id)
    if not file_record or file_record.owner != current_user:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    file_content = file.file.read()
    s3_service.upload_file(file_id, file_content)
    return {"message": "Contenido del archivo cargado correctamente"}

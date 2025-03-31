from typing import Optional
from pydantic import BaseModel

class FileRecord(BaseModel):
    id: str
    filename: str
    description: Optional[str] = None
    owner: str  # Corresponde al email del usuario

# Base de datos en memoria para archivos (sólo para demo)
files_db = {}

def create_file(file_record: FileRecord) -> FileRecord:
    files_db[file_record.id] = file_record
    return file_record

def get_file(file_id: str):
    return files_db.get(file_id)

def delete_file(file_id: str):
    return files_db.pop(file_id, None)

def list_files(owner: str):
    return [file for file in files_db.values() if file.owner == owner]

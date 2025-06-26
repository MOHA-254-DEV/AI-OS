from fastapi import APIRouter, Depends, File as UploadFile, UploadFile, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os

from app.schemas.file import FileCreate, FileUpdate, FileOut
from app.crud.file import (
    create_file, get_file, get_files_by_path, get_files_by_owner, update_file, delete_file
)
from app.api.deps import get_db, get_current_active_user
from app.core.utils import save_file, delete_file as delete_file_storage

router = APIRouter()

@router.get("/", response_model=List[FileOut])
def list_my_files(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
):
    return get_files_by_owner(db, current_user.id, skip=skip, limit=limit)

@router.post("/upload", response_model=FileOut)
def upload_file(
    file: UploadFile = File(...),
    path: str = Form(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    filename = file.filename
    storage_path = os.path.join(path, filename)
    file_url = save_file(storage_path, file.file)
    file_data = FileCreate(
        name=filename,
        path=path,
        type="file",
        size=file.spool_max_size,
        preview_url=file_url
    )
    return create_file(db, file_data, current_user.id)

@router.patch("/{file_id}", response_model=FileOut)
def update_file_info(
    file_id: str,
    file_update: FileUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    db_file = get_file(db, file_id)
    if not db_file or db_file.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="File not found")
    return update_file(db, db_file, file_update)

@router.delete("/{file_id}", response_model=dict)
def delete_file_by_id(
    file_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user),
):
    db_file = get_file(db, file_id)
    if not db_file or db_file.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="File not found")
    delete_file_storage(db_file.path)
    delete_file(db, db_file)
    return {"msg": "File deleted"}

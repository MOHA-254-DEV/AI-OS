from fastapi import APIRouter, Depends, HTTPException, UploadFile, File as FastAPIFile
from sqlalchemy.orm import Session
from typing import List
from app.schemas.file import FileOut, FileCreate
from app.crud.file import get_file, get_files_for_org, get_files_for_user, create_file, delete_file
from app.api.deps import get_db, get_current_user
import shutil
import os

router = APIRouter()

@router.get("/", response_model=List[FileOut])
def list_files(organization_id: int, db: Session = Depends(get_db)):
    return get_files_for_org(db, organization_id=organization_id)

@router.get("/{file_id}", response_model=FileOut)
def retrieve_file(file_id: int, db: Session = Depends(get_db)):
    file = get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file

@router.post("/", response_model=FileOut)
def upload_file(
    organization_id: int,
    owner_id: int,
    upload: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db)
):
    upload_dir = f"./app/static/files/org_{organization_id}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, upload.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)
    file_in = FileCreate(
        filename=upload.filename,
        size=os.path.getsize(file_path),
        owner_id=owner_id,
        organization_id=organization_id,
        path=file_path,
    )
    return create_file(db, file=file_in)

@router.delete("/{file_id}")
def delete_file_api(file_id: int, db: Session = Depends(get_db)):
    db_file = get_file(db, file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    return delete_file(db, db_file)

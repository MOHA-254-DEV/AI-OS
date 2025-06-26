from sqlalchemy.orm import Session
from typing import Optional, List
from app.db.models.file import File
from app.schemas.file import FileCreate, FileUpdate

def get_file(db: Session, file_id):
    return db.query(File).filter(File.id == file_id).first()

def get_files_by_path(db: Session, path: str) -> List[File]:
    return db.query(File).filter(File.path == path).all()

def get_files_by_owner(db: Session, owner_id, skip: int = 0, limit: int = 100) -> List[File]:
    return db.query(File).filter(File.owner_id == owner_id).offset(skip).limit(limit).all()

def create_file(db: Session, file: FileCreate, owner_id):
    db_file = File(
        name=file.name,
        path=file.path,
        type=file.type,
        size=file.size or 0,
        modified=file.modified,
        preview_url=file.preview_url,
        owner_id=owner_id,
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def update_file(db: Session, db_file: File, file_update: FileUpdate):
    for field, value in file_update.dict(exclude_unset=True).items():
        setattr(db_file, field, value)
    db.commit()
    db.refresh(db_file)
    return db_file

def delete_file(db: Session, db_file: File):
    db.delete(db_file)
    db.commit()
    return True

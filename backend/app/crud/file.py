from sqlalchemy.orm import Session
from app.db.models.file import File
from app.schemas.file import FileCreate

def get_file(db: Session, file_id: int):
    return db.query(File).filter(File.id == file_id).first()

def get_files_for_org(db: Session, organization_id: int, skip: int = 0, limit: int = 100):
    return db.query(File).filter(File.organization_id == organization_id).offset(skip).limit(limit).all()

def get_files_for_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(File).filter(File.owner_id == user_id).offset(skip).limit(limit).all()

def create_file(db: Session, file: FileCreate):
    db_file = File(
        filename=file.filename,
        size=file.size,
        owner_id=file.owner_id,
        organization_id=file.organization_id,
        path=file.path,
        is_deleted=file.is_deleted,
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def delete_file(db: Session, db_file: File):
    db_file.is_deleted = True
    db.commit()
    db.refresh(db_file)
    return db_file

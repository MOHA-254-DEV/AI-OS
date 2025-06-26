import os
import shutil
import boto3
from botocore.exceptions import ClientError
from typing import Optional, Tuple
from app.core.config import settings

def save_file_local(save_path: str, file_obj) -> str:
    """Save file to local disk."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file_obj, f)
    return save_path

def delete_file_local(file_path: str):
    """Delete file from local disk."""
    if os.path.exists(file_path):
        os.remove(file_path)

def save_file_s3(filename: str, file_obj) -> str:
    """Save file to S3 bucket."""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION,
    )
    try:
        s3.upload_fileobj(file_obj, settings.S3_BUCKET, filename)
        url = f"https://{settings.S3_BUCKET}.s3.{settings.S3_REGION}.amazonaws.com/{filename}"
        return url
    except ClientError as e:
        raise RuntimeError(f"S3 upload failed: {e}")

def delete_file_s3(filename: str):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION,
    )
    try:
        s3.delete_object(Bucket=settings.S3_BUCKET, Key=filename)
    except ClientError as e:
        raise RuntimeError(f"S3 delete failed: {e}")

def get_storage_backend() -> str:
    """Returns 'local' or 's3' depending on configuration."""
    return settings.FILES_STORAGE

def save_file(filename: str, file_obj) -> str:
    if get_storage_backend() == "local":
        save_path = os.path.join(settings.FILES_LOCAL_PATH, filename)
        return save_file_local(save_path, file_obj)
    else:
        return save_file_s3(filename, file_obj)

def delete_file(filename: str):
    if get_storage_backend() == "local":
        file_path = os.path.join(settings.FILES_LOCAL_PATH, filename)
        delete_file_local(file_path)
    else:
        delete_file_s3(filename)

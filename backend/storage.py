import boto3
import uuid
from botocore.client import Config

MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
BUCKET_NAME = "basket" 

def upload_image(file_bytes: bytes, filename: str) -> str:
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4"),
    )
    key = f"products/{uuid.uuid4()}_{filename}"
    
    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=file_bytes)
    return key

def get_image(key: str):
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4"),
    )
    response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    return response["Body"].read()
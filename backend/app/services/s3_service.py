import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import logging
from typing import BinaryIO, Optional
from ..core.config import settings

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            config=Config(signature_version='s3v4'),
            region_name='us-east-1'
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"Bucket {self.bucket_name} already exists")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                try:
                    self.client.create_bucket(Bucket=self.bucket_name)
                    logger.info(f"Created bucket {self.bucket_name}")
                except ClientError as create_error:
                    logger.error(f"Failed to create bucket: {create_error}")
                    raise
            else:
                logger.error(f"Error checking bucket: {e}")
                raise
    
    async def upload_file(
        self,
        file_data: BinaryIO,
        object_key: str,
        content_type: str
    ) -> str:
        """
        Upload a file to S3
        
        Args:
            file_data: File binary data
            object_key: S3 object key (path)
            content_type: MIME type of the file
            
        Returns:
            S3 path (bucket/key)
        """
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=file_data,
                ContentType=content_type
            )
            logger.info(f"Uploaded file to s3://{self.bucket_name}/{object_key}")
            return f"{self.bucket_name}/{object_key}"
        except ClientError as e:
            logger.error(f"Failed to upload file: {e}")
            raise
    
    async def download_file(self, object_key: str) -> bytes:
        """
        Download a file from S3
        
        Args:
            object_key: S3 object key (path)
            
        Returns:
            File binary data
        """
        try:
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            return response['Body'].read()
        except ClientError as e:
            logger.error(f"Failed to download file: {e}")
            raise
    
    async def delete_file(self, object_key: str) -> bool:
        """
        Delete a file from S3
        
        Args:
            object_key: S3 object key (path)
            
        Returns:
            True if successful
        """
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=object_key
            )
            logger.info(f"Deleted file s3://{self.bucket_name}/{object_key}")
            return True
        except ClientError as e:
            logger.error(f"Failed to delete file: {e}")
            return False
    
    async def get_file_url(self, object_key: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL for file access
        
        Args:
            object_key: S3 object key (path)
            expiration: URL expiration time in seconds (default 1 hour)
            
        Returns:
            Presigned URL
        """
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_key
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            raise

# Singleton instance
s3_service = S3Service()


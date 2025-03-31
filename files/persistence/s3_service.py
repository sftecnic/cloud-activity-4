import os
import boto3

class S3Service:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("S3_ENDPOINT_URL", "http://minio:9000"),
            aws_access_key_id=os.getenv("S3_ACCESS_KEY", "minioadmin"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY", "minioadmin"),
            region_name="us-east-1"
        )
        self.bucket = os.getenv("S3_BUCKET", "files")
        self._create_bucket()

    def _create_bucket(self):
        buckets = [bucket["Name"] for bucket in self.s3.list_buckets().get("Buckets", [])]
        if self.bucket not in buckets:
            self.s3.create_bucket(Bucket=self.bucket)

    def upload_file(self, file_id: str, file_content: bytes):
        self.s3.put_object(Bucket=self.bucket, Key=file_id, Body=file_content)

    def download_file(self, file_id: str) -> bytes:
        response = self.s3.get_object(Bucket=self.bucket, Key=file_id)
        return response["Body"].read()

    def delete_file(self, file_id: str):
        self.s3.delete_object(Bucket=self.bucket, Key=file_id)

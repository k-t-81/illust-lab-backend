from boto3 import client
from pydantic import BaseModel


class ImageUpload(BaseModel):
    bucket: str
    key: str
    endpoint_url: str
    image: bytes


aws_access_key_id = "minio_root"
aws_secret_access_key = "minio_password"
region_name = ""


# S3に画像をアップロードする関数
def upload_image(data: ImageUpload) -> str:
    s3 = client(
        "s3",
        endpoint_url=data.endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )

    s3.put_object(
        Body=data.image,
        Bucket=data.bucket,
        Key=data.key,
        ContentType="image/png"
    )

    return f"{data.endpoint_url}/{data.bucket}/{data.key}"

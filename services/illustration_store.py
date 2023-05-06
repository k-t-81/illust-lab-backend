import datetime
from io import BytesIO

import requests
from PIL import Image
from pydantic import BaseModel

import libs.s3 as s3


# S3にアップロードするためのpydanticモデル
class IllustrationUpload(BaseModel):
    path: str
    image: bytes


# S3からダウンロードするためのpydanticモデル
class IllustrationDownload(BaseModel):
    path: str


# S3の設定
bucket = "stable-diffusion-v2.1"
key = "output"
endpoint_url = "http://localhost:9000"


# S3にアップロード
def upload_illustration(data: IllustrationUpload) -> str:
    # 日時をファイル名に付与
    date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # S3にアップロード
    return s3.upload_image(s3.ImageUpload(
        image=data.image,
        bucket=bucket,
        key=f"{key}/{date}_{data.path}",
        endpoint_url=endpoint_url
    ))


# S3からダウンロード
def download_illustration(data: IllustrationDownload) -> bytes:
    # data.pathがendpoint_url/bucket/key/を含んでいるか確認
    if data.path.startswith(f"{endpoint_url}/{bucket}/{key}/"):
        # 含んでいる場合はそのままリクエストを送信
        response = requests.get(data.path)
    else:
        response = requests.get(f"{endpoint_url}/{bucket}/{key}/{data.path}")

    # バイナリデータをPIL.Imageに変換
    image = Image.open(BytesIO(response.content))
    image_bytes = BytesIO()
    # PNG形式で保存
    image.save(image_bytes, format="PNG")
    # バイト列に変換
    return image_bytes.getvalue()

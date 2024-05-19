from django.utils.deconstruct import deconstructible
import uuid
import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from user_backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


# Генерация имен для изображений
@deconstructible
class HashedUploadTo(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        filename_base, filename_ext = os.path.splitext(filename)
        return f"{self.path}{filename_base}-{uuid.uuid4()}{filename_ext}"


# Коррекция перекоса
def deskew_image(image):
    pass


# Получить изображения
def get_from_s3(key) -> str:
    client = boto3.client("s3",
                          endpoint_url='http://minio:9000',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          config=Config(signature_version='s3v4'),
                          region_name='us-west-rack-2'
                          )
    try:
        filename = f'/tmp/{key.split("/")[-1]}'
        client.download_file(Bucket="static",
                             Key=key,
                             Filename=filename)

    except ClientError as exc:
        print(
            f"Can't find {key}. Reason: {exc}"
        )

    return filename

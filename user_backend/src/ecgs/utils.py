import tempfile

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.deconstruct import deconstructible
import uuid
import os
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from user_backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from io import BytesIO

from PIL import Image
from skimage import io
from skimage.color import rgb2gray
from skimage.transform import rotate
import numpy as np
from deskew import determine_skew


# Генерация имен для изображений
@deconstructible
class HashedUploadTo(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        filename_base, filename_ext = os.path.splitext(filename)
        return f"{self.path}{filename_base}-{uuid.uuid4()}{filename_ext}"


# Коррекция перекоса
def deskew_image(input_image):
    image = io.imread(input_image.file)
    is_photo = True
    if image.shape[2] == 4:
        # проблема синтетических данных: они читаются в RGBA, A удалить
        image = image[:, :, :3]
        is_photo = False

    grayscale = rgb2gray(image)
    angle = determine_skew(grayscale)
    rotated = rotate(image, angle, resize=True) * 255

    rotated_image = Image.fromarray(rotated.astype(np.uint8))
    if is_photo:
        # проблема несинтетических данных: np путает высоту и ширину, поэтому поворот
        rotated_image = rotated_image.rotate(-90, expand=True)

    # Упаковать в InMemoryUploadedFile
    image_io = BytesIO()
    rotated_image.save(image_io, format='PNG')
    image_file = InMemoryUploadedFile(image_io, None, input_image._name, input_image.content_type, image_io.tell, None)
    return image_file


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

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from settings import settings

client = boto3.client("s3",
                      endpoint_url='http://minio:9000',
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                      config=Config(signature_version='s3v4'),
                      region_name='us-west-rack-2'
                      )


def get_from_s3(key, bucket) -> str:
    try:
        filename = f'/tmp/{key.split("/")[-1]}'
        client.download_file(Bucket=bucket,
                             Key=key,
                             Filename=filename)

    except ClientError as exc:
        print(
            f"Can't find {key}. Reason: {exc}"
        )

    return filename



def save_ecg_to_s3(header_file_path, signal_file_path):
    client.upload_file()

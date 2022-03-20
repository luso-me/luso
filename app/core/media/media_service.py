import os.path
from typing import IO

import boto3
import shortuuid  # type: ignore
import structlog
from botocore.config import Config

log = structlog.get_logger()


class MediaService:
    def __init__(self, region: str, bucket_name: str, random_suffix=False):
        self.s3 = boto3.resource("s3", config=Config(region_name=region))
        self.region = region
        self.bucket_name = bucket_name
        self.bucket = self.s3.Bucket(bucket_name)
        self.random_suffix = random_suffix
        self.s3_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com"

    async def upload_image(self, image_name: str, bytes_: IO) -> str:
        suffix = ""
        if self.random_suffix:
            suffix = shortuuid.random()

        basename, ext = os.path.splitext(image_name)

        if suffix:
            filename = f"{basename}-{suffix}{ext}"
        else:
            filename = f"{basename}{ext}"

        log.info(f"Uploading image, {filename} to S3")
        self.bucket.upload_fileobj(bytes_, filename)

        return f"{self.s3_url}/{filename}"

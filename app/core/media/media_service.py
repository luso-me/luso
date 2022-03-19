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

    async def upload_image(self, image_name: str, bytes_: IO):
        log.info(f"Uploading image, {image_name} to S3")

        suffix = ""
        if self.random_suffix:
            suffix = shortuuid.random()

        basename, ext = os.path.splitext(image_name)
        self.bucket.upload_fileobj(bytes_, f"{basename}-{suffix}{ext}")

        return (
            f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com"
            f"/{basename}-{suffix}{ext}"
        )

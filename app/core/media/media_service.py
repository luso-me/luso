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
        filename = self._determine_filename(basename, ext, suffix)
        self._upload_object(bytes_, ext, filename)

        return f"{self.s3_url}/{filename}"

    def _determine_filename(self, basename, ext, suffix):
        if suffix:
            return f"{basename}-{suffix}{ext}"
        else:
            return f"{basename}{ext}"

    def _upload_object(self, bytes_, ext, filename):
        log.info(f"Uploading image, {filename} to S3")

        if ext == ".svg":
            self.bucket.upload_fileobj(
                bytes_, filename, ExtraArgs={"ContentType": "image/svg+xml"}
            )
        else:
            self.bucket.upload_fileobj(bytes_, filename)

import os.path
import urllib
from typing import IO
from urllib.parse import quote_plus

import boto3
import shortuuid  # type: ignore
import structlog
from botocore.config import Config

log = structlog.get_logger()


class MediaService:
    def __init__(self, region: str, bucket_name: str):
        self.s3 = boto3.resource("s3", config=Config(region_name=region))
        self.region = region
        self.bucket_name = bucket_name
        self.bucket = self.s3.Bucket(bucket_name)

        self.s3_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com"

    async def upload_image(self, image_name: str, bytes_: IO) -> str:
        basename, ext = os.path.splitext(image_name)
        self._upload_object(bytes_, ext, image_name)

        return (
            f"""{self.s3_url}/{urllib.parse.quote_plus(image_name, safe="!-_.*'()")}"""
        )

    def _upload_object(self, bytes_, ext, filename):
        log.info(f"Uploading image [{filename}] to S3")

        if ext == ".svg":
            self.bucket.upload_fileobj(
                bytes_, filename, ExtraArgs={"ContentType": "image/svg+xml"}
            )
        else:
            self.bucket.upload_fileobj(bytes_, filename)

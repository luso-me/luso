import os.path
from typing import IO

import boto3
import shortuuid
import structlog
from botocore.config import Config

from app.config import settings

log = structlog.get_logger()


class MediaService:

    def __init__(self):
        self.s3 = boto3.client('s3',
                               config=Config(
                                   region_name=settings.icons_s3_bucket_region
                               ))

    async def upload_image(self, image_name: str, bytes_: IO):
        suffix = shortuuid.random()
        basename, ext = os.path.splitext(image_name)
        self.s3.upload_fileobj(bytes_, settings.icons_s3_bucket, f'{basename}-{suffix}{ext}')
        return f'https://luso-me-media-local.s3.{settings.icons_s3_bucket_region}.amazonaws.com/{basename}-{suffix}{ext}'

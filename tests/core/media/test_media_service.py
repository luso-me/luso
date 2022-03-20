import re
import io
from unittest import mock

import pytest

from app.core.media.media_service import MediaService

bucket = "some-bucket"
region = "some-region"
s3_url = f"https://{bucket}.s3.{region}.amazonaws.com"


@pytest.mark.asyncio
@mock.patch("boto3.resource")
async def test_upload_image(mock_boto_resource):
    img_content = io.BytesIO(b"hello world: \x00\x01")

    # with random suffix
    media_service = MediaService(region, bucket, True)
    result = await media_service.upload_image("img.png", img_content)
    assert re.match(
        r"(https://some-bucket\.s3\.some-region\.amazonaws\.com/img-.{22}.png)", result
    )

    # without suffix
    media_service = MediaService(region, bucket)
    result = await media_service.upload_image("img.png", img_content)
    assert result == f"{s3_url}/img.png"

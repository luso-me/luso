import io
from unittest import mock

import pytest

from app.core.media.media_service import MediaService


@pytest.mark.asyncio
@mock.patch("boto3.resource")
async def test_upload_image(mock_boto_resource):
    media_service = MediaService("some-region", "some-bucket")

    img_content = io.BytesIO(b"hello world: \x00\x01")
    result = await media_service.upload_image("img.png", img_content)

    assert result == "https://some-bucket.s3.some-region.amazonaws.com/img.png"

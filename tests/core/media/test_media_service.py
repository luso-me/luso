import io
from unittest import mock

import pytest

from app.core.media.media_service import MediaService

bucket = "some-bucket"
region = "some-region"
s3_url = f"https://{bucket}.s3.{region}.amazonaws.com"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "filename, url",
    [
        ("test 123.png", f"{s3_url}/test+123.png"),
        ("test++.png", f"{s3_url}/test%2B%2B.png"),
        ("test.png", f"{s3_url}/test.png"),
        ("test#.png", f"{s3_url}/test%23.png"),
        ("~test*()!.png", f"{s3_url}/~test*()!.png"),
    ],
)
@mock.patch("boto3.resource")
async def test_upload_image(mock_boto_resource, filename, url):
    img_content = io.BytesIO(b"hello world: \x00\x01")

    media_service = MediaService(region, bucket)
    result = await media_service.upload_image(filename, img_content)
    assert result == url

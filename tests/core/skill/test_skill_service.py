import io
from unittest import mock

import pytest

from app.core.skill.skill_service import SkillService
from tests.test_helper import create_skill_multiple_resources

skill_service = SkillService()


@pytest.mark.asyncio
@mock.patch("app.core.media.media_service.MediaService.upload_image")
@mock.patch("app.repositories.skill.SkillRepository.update")
async def test_update_skill_icon(mock_media_service, mock_skill_repo):
    # mock_media_service.return_value = "https://s3.com/some-icon-link.svg"
    mock_skill_repo.return_value = _create_skill()

    # step 1: prove that the current code fails

    # get the resources on the return value

    img_content = io.BytesIO(b"hello world: \x00\x01")
    x = await skill_service.update_skill_icon(
        "123", "some-skill", "some_icon", img_content
    )
    assert len(x.resources) == 2

    # step 2: change the code so that it passes


def _create_skill():
    return create_skill_multiple_resources()

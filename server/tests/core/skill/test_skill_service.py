import io
from unittest import mock

import pytest

from app.core.skill.skill_service import SkillService
from tests.test_helper import create_skill_multiple_resources

skill_service = SkillService()


@pytest.mark.asyncio
@mock.patch("app.core.media.media_service.MediaService.upload_image")
@mock.patch("app.repositories.skill.SkillRepository.update")
@mock.patch("app.core.skill.skill_service.SkillService.get_skill")
async def test_update_skill_icon(
    mock_media_service, mock_skill_repo, mock_skill_service
):
    skill = _create_skill()
    mock_skill_repo.return_value = skill

    result_skill = await skill_service.update_skill_icon(
        "123", "some-skill", "some_icon", io.BytesIO(b"hello world: \x00\x01")
    )
    assert len(result_skill.resources) == 2


def _create_skill():
    return create_skill_multiple_resources()

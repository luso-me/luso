import pytest
from motor import motor_asyncio

from app.config import settings
from app.repositories.skill import SkillsRepository
from app.schema.skill import InSkill


@pytest.fixture(scope='session')
def skill_repo():
    client = motor_asyncio.AsyncIOMotorClient(settings.mongo_connection_url)
    skill_repo = SkillsRepository(client, db_name='luso', collection='skills')
    yield skill_repo


@pytest.mark.asyncio
async def test_skill_repo(skill_repo):
    skill = InSkill(name='test', description='test', tags=[], web_link='')
    new_skill = await skill_repo.create(skill)
    print(new_skill)


@pytest.mark.asyncio
async def test_find_by_skill_id(skill_repo):
    skill = await skill_repo.find_by_key('id', 'eyWdhrTDmPQrT7FzV4E5wn')
    print(skill)

import asyncio
import json

from app.core.skill.model.base import SkillCreate
from app.core.user.model.base import UserCreate
from app.database import get_db_client
from app.repositories.skill import SkillRepository
from app.repositories.user import UserRepository


async def populate_db():
    with open("../test_resources/sample.json") as file:
        data = json.load(file)
        await insert_skills(data)
        await insert_users(data)


async def insert_skills(data):
    print("Inserting Skills")
    repo = SkillRepository(
        db_client_factory=get_db_client, db_name="luso", collection_name="skills"
    )

    for skill in data["skills"]:
        s = SkillCreate(
            name=skill["name"],
            description=skill["description"],
            web_link=skill["web_link"],
            repo_link=skill["repo_link"],
            icon_link=skill["icon_link"],
            tags=skill["tags"],
            category=skill["category"],
            active=skill["active"],
            resources=skill["resources"],
        )
        await repo.create(s)


async def insert_users(data):
    print("Inserting Users")
    repo = UserRepository(
        db_client_factory=get_db_client, db_name="luso", collection_name="users"
    )

    for user in data["users"]:
        u = UserCreate(
            username=user["username"],
            github_user_id=user["github_user_id"],
            display_name=user["display_name"],
            email=user["email"],
            active=user["active"],
            score=user["score"],
            skills=user["skills"],
            plans=user["plans"],
        )
        await repo.create(u)


asyncio.run(populate_db())

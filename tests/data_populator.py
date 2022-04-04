import asyncio
import json
from typing import List

from app.core.skill.model.base import SkillCreate, SkillRead
from app.core.skill.skill_service import SkillService
from app.core.user import user_service
from app.core.user.model.base import UserCreate
from app.database import get_db_client
from app.repositories.skill import SkillRepository

skill_repo = SkillRepository(
    db_client_factory=get_db_client, db_name="luso", collection_name="skills"
)

skill_service = SkillService()


async def populate_db():
    with open("../test_resources/sample.json") as file:
        data = json.load(file)
        await insert_skills(data)
        await insert_users(data)


async def insert_skills(data):
    print("Inserting Skills")

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
        await skill_service.create_skill(s)


async def insert_users(data):
    print("Inserting Users")
    airflows: List[SkillRead] = await skill_repo.find({"name": "Apache Airflow"})

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

        u.skills[0].skill_id = airflows[0].id
        u.plans[0].skill_id = airflows[0].id
        u.plans[0].objectives[0].resource_id = airflows[0].resources[0].id
        u.plans[0].objectives[0].resource_item_id = airflows[0].resources[0].items[0].id

        u.plans[0].objectives[1].resource_id = airflows[0].resources[1].id
        u.plans[0].objectives[1].resource_item_id = airflows[0].resources[1].items[0].id

        await user_service.create_user(u)


asyncio.run(populate_db())

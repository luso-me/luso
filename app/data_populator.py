import json
import pymongo

from app.adapters.dependencies.db import skill_repository
from app.core.skill.models.base import SkillCreate
from app.core.user.model.base import UserCreate
from app.database import get_db_client
from app.repositories.skill import SkillRepository


def populate_db():
    with open("../test_resources/sample.json") as file:
        data = json.load(file)
        insert_skills(data)
        # insert_users(data, mydb)


def insert_skills(data):
    repo = SkillRepository(db_client_factory=get_db_client, db_name='luso',
                           collection_name='skills')

    for skill in data["skills"]:
        s = SkillCreate(name=skill["name"],
                        description=skill["description"],
                        web_link=skill["web_link"],
                        repo_link=skill["repo_link"],
                        icon_link=skill["icon_link"],
                        tags=skill["tags"],
                        category=skill["category"],
                        active=skill["active"],
                        resources=skill["resources"])
        print(skill)
        repo.create(s)
        # mydb.mycoll.insert_one(s)
        # s_repo.create(s)


def insert_users(data, mydb):
    print("Inserting users")
    for user in data["users"]:
        u = UserCreate(name=user["name"],
                       description=user["description"],
                       web_link=user["web_link"],
                       repo_link=user["repo_link"],
                       icon_link=user["icon_link"],
                       tags=user["tags"],
                       active=user["active"])
        print(user)
        mydb.mycoll.insert_one(u)
        # s_repo.create(s)


populate_db()

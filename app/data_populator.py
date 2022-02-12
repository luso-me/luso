import json
import pymongo

from app.core.skill.models.base import SkillCreate


def populate_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["luso"]
    print(client.list_database_names())

    with open("../test_resources/sample.json") as file:
        data = json.load(file)
        insert_skills(data, mydb)
        insert_users(data, mydb)


def insert_skills(data, mydb):
    print("Inserting skills")
    for skill in data["skills"]:
        s = SkillCreate(name=skill["name"],
                        description=skill["description"],
                        web_link=skill["web_link"],
                        repo_link=skill["repo_link"],
                        icon_link=skill["icon_link"],
                        tags=skill["tags"],
                        active=skill["active"])
        print(skill)
        mydb.mycoll.insert_one(s)
        # s_repo.create(s)


def insert_users(data, mydb):
    print("Inserting users")
    for skill in data["users"]:
        s = SkillCreate(name=skill["name"],
                        description=skill["description"],
                        web_link=skill["web_link"],
                        repo_link=skill["repo_link"],
                        icon_link=skill["icon_link"],
                        tags=skill["tags"],
                        active=skill["active"])
        print(skill)
        mydb.mycoll.insert_one(s)
        # s_repo.create(s)


populate_db()

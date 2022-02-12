import json
import pymongo

from app.core.skill.models.base import SkillCreate


def populate_db():
    # todo: nothing is inserted into db
    # s_repo = SkillRepository(db_session=client, db_name='luso',
    #                          collection='skills')
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = client["luso"]  # you can also use dot notation client.mydatabase
    print(client.list_database_names())

    with open("../test_resources/sample.json") as file:
        data = json.load(file)
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

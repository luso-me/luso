import json
from app.core.skill.model.base import SkillUpdate
import os
from typing import Any

test_skills = "test_resources/skills"


def file_to_json(path) -> Any:
    from app.config import settings

    with open(os.path.join(settings.base_dir, path), "r") as f:
        data = f.read()
        return json.loads(data)


def create_skill_multiple_resources() -> SkillUpdate:
    s = file_to_json("test_resources/skills/test-skill-multiple-resources/skill.json")
    return SkillUpdate(**s)

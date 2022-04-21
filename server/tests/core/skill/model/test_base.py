from server.app.core.skill.model.base import SkillUpdate, SkillCreate
from datetime import datetime

from server.app.core.skill.model.resource import SkillResource, SkillResourceItem


def test_generate_icon_name():
    skill = SkillUpdate()
    icon_name = "file.svg"

    result = skill.generate_icon_name("skill-x", icon_name)
    assert result == "skill-x.svg"

    result = skill.generate_icon_name("Skill X", icon_name)
    assert result == "skill x.svg"

    result = skill.generate_icon_name("Skill X Y", icon_name)
    assert result == "skill x y.svg"

    result = skill.generate_icon_name("Skill X:Y", icon_name)
    assert result == "skill x:y.svg"

    result = skill.generate_icon_name("SkillX", icon_name)
    assert result == "skillx.svg"

    result = skill.generate_icon_name("s++", icon_name)
    assert result == "s++.svg"


def test_set_default_values():
    r1 = _create_resource("r1")
    r2 = _create_resource("r2")

    skill = SkillCreate(
        description="s-desc-123",
        web_link="s-link",
        category="s-cat",
        name="test-skills",
        active=True,
        resources=[r1, r2],
    )
    skill.set_default_values(skill)

    assert type(r1.resource_added_date) == datetime
    assert type(r2.resource_added_date) == datetime

    assert len(r1.id) == 22
    assert len(r1.items[0].id) == 22
    assert len(r1.items[1].id) == 22

    assert len(r2.id) == 22
    assert len(r2.items[0].id) == 22
    assert len(r2.items[1].id) == 22


def _create_resource(identifier: str):
    return SkillResource(
        name=identifier,
        description=f"{identifier}-desc",
        category="r-cat",
        authors=f"{identifier}-auth",
        web_link=f"{identifier}-link",
        items=_create_items(2, identifier),
    )


def _create_items(count: int, identifier: str):
    items = []
    for i in range(count):
        items.append(
            SkillResourceItem(
                name=f"{identifier}-item-{i}", description=f"{identifier}-desc-{i}"
            )
        )

    return items

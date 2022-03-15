from datetime import datetime

from app.core.skill import skill_service
from app.core.skill.model.base import SkillCreate
from app.core.skill.model.resource import SkillResource, SkillResourceItem


def test_set_default_values():
    r1 = _create_resource("r1")
    r2 = _create_resource("r2")

    skill = SkillCreate(
        description="s-desc-123",
        web_link="s-link",
        category="s-cat",
        name="test-skill",
        active=True,
        resources=[r1, r2],
    )
    skill_service._set_default_values(skill)

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
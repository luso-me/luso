from datetime import datetime

import pytest

from app.core.user.model.base import UserRead, UserUpdate
from app.core.user.model.skill_plan import SkillPlan, SkillPlanObjective
from app.core.user.model.user_score import UserScore
from app.core.user.user_service import UserService


@pytest.fixture
def user_service():
    return UserService()


@pytest.mark.parametrize(
    ["current_status", "new_status", "expected"],
    [
        ("Todo", "Todo", UserScore(gold=1, points=1)),
        ("Todo", "Done", UserScore(gold=2, points=2)),
        ("In Progress", "Todo", UserScore(gold=1, points=1)),
        ("In Progress", "Todo", UserScore(gold=1, points=1)),
        ("In Progress", "Done", UserScore(gold=2, points=2)),
        ("Done", "Done", UserScore(gold=1, points=1)),
        ("Done", "In Progress", UserScore(gold=0, points=0)),
        ("Done", "Todo", UserScore(gold=0, points=0)),
    ],
)
def test_update_user_score(user_service, current_status, new_status, expected):
    user_db: UserRead = UserRead(
        id="123456789abcdefgihter8",
        email="123@123.com",
        github_user_id="1234",
        username="jack",
        score=UserScore(gold=1, points=1),
        plans=[
            SkillPlan(
                id="123",
                plan_name="conquer and divide",
                skill_id="123",
                start_date=datetime.fromisocalendar(2022, 1, 1),
                end_date=datetime.fromisocalendar(2022, 1, 6),
                time_horizon="3 - 6 months",
                status="",
                objectives=[
                    SkillPlanObjective(
                        id="1",
                        resource_id="123",
                        resource_item_id="1",
                        status=current_status,
                    ),
                ],
            )
        ],
    )

    user_update: UserUpdate = UserUpdate(
        score=UserScore(gold=100, points=10),
        plans=[
            SkillPlan(
                id="123",
                plan_name="conquer and divide",
                skill_id="123",
                start_date=datetime.fromisocalendar(2022, 1, 1),
                end_date=datetime.fromisocalendar(2022, 1, 6),
                time_horizon="3 - 6 months",
                status="",
                objectives=[
                    SkillPlanObjective(
                        id="1",
                        resource_id="123",
                        resource_item_id="456",
                        status=new_status,
                    )
                ],
            )
        ],
    )

    user_service._set_user_score(user_db, user_update)

    assert user_update.score == expected


@pytest.mark.parametrize(
    ["new_status", "expected"],
    [
        ("Done", UserScore(gold=16, points=16)),
        ("In Progress", UserScore(gold=15, points=15)),
        ("Todo", UserScore(gold=15, points=15)),
    ],
)
def test_update_user_score_new_objective(user_service, new_status, expected):
    user_db: UserRead = UserRead(
        id="123456789abcdefgihter8",
        email="123@123.com",
        github_user_id="1234",
        username="jack",
        score=UserScore(gold=14, points=14),
        plans=[
            SkillPlan(
                id="spid1",
                plan_name="conquer and divide",
                skill_id="sid1",
                start_date=datetime.fromisocalendar(2022, 1, 1),
                end_date=datetime.fromisocalendar(2022, 1, 6),
                time_horizon="3 - 6 months",
                status="",
                objectives=[
                    SkillPlanObjective(
                        id="spoid1",
                        resource_id="123",
                        resource_item_id="1",
                        status="Todo",
                    ),
                ],
            )
        ],
    )

    user_update: UserUpdate = UserUpdate(
        score=UserScore(gold=100, points=10),
        plans=[
            SkillPlan(
                id="spid1",
                plan_name="conquer and divide",
                skill_id="sid1",
                start_date=datetime.fromisocalendar(2022, 1, 1),
                end_date=datetime.fromisocalendar(2022, 1, 6),
                time_horizon="3 - 6 months",
                status="",
                objectives=[
                    SkillPlanObjective(
                        id="spoid1",
                        resource_id="123",
                        resource_item_id="1",
                        status="Done",
                    ),
                    SkillPlanObjective(
                        id="spoid2",
                        resource_id="123",
                        resource_item_id="1",
                        status=new_status,
                    ),
                ],
            )
        ],
    )

    user_service._set_user_score(user_db, user_update)

    assert user_update.score == expected

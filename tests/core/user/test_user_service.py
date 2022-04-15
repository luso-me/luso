from datetime import datetime

import pytest

from app.core.user.model.base import UserRead, UserUpdate
from app.core.user.model.skill_plan import SkillPlan
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
        ("In progress", "Todo", UserScore(gold=1, points=1)),
        ("In progress", "Todo", UserScore(gold=1, points=1)),
        ("In progress", "Done", UserScore(gold=2, points=2)),
        ("Done", "Done", UserScore(gold=1, points=1)),
        ("Done", "In progress", UserScore(gold=0, points=0)),
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
                status=current_status,
                objectives=[s],
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
                status=new_status,
            )
        ],
    )

    user_service._set_user_points(user_db, user_update)

    assert user_update.score == expected

from dataclasses import dataclass
from typing import Optional

from volcano.domain.entity.todo import Todo


@dataclass
class TodayGoalObject:
    today_goal_percentage: Optional[int] = None
    today_todo: Optional[list[Todo]] = None


@dataclass
class MonthGoalObject:
    month_goal_percentage: Optional[int] = None
    month_todo: Optional[list[Todo]] = None


@dataclass
class GoalInfo:
    today_goal: Optional[TodayGoalObject] = None
    month_goal: Optional[MonthGoalObject] = None

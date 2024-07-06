from dataclasses import dataclass
from typing import Optional


@dataclass
class GoalPercentage:
    today_goal_percentage: Optional[int] = None
    month_goal_percentage: Optional[int] = None

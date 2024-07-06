from dataclasses import dataclass
from typing import Optional

from volcano.domain.entity.todo import Todo


@dataclass
class ReadTodo:
    type: Optional[str] = None
    values: Optional[list[Todo]] = None

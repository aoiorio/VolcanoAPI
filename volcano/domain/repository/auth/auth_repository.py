from abc import ABC, abstractmethod
from typing import Optional
from ...entity.user import VolcanoUserEntity

from pydantic.dataclasses import dataclass

class AuthRepository(ABC):
    volcano_user_entity: VolcanoUserEntity
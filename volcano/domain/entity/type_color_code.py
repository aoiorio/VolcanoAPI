from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class TypeColorCode:
    id: Optional[int] = None
    color_id: Optional[str] = None
    type: Optional[str] = None
    start_color_code: Optional[str] = None
    end_color_code: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

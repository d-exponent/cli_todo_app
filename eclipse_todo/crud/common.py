from dataclasses import dataclass
from datetime import datetime


@dataclass
class TodoEntry:
    todo: str
    due: datetime | None = None

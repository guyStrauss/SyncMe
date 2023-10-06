"""
Represents an event that occurred in the directory.
"""
import datetime
import enum
from typing import Optional

from pydantic import BaseModel


class EventType(enum.Enum):
    STARTUP = "STARTUP"
    CREATED = "CREATED"
    DELETED = "DELETED"
    MODIFIED = "MODIFIED"
    MOVED = "MOVED"
    ROUTINE_CHECK = "ROUTINE_CHECK"


class Event(BaseModel):
    type: EventType
    time: Optional[datetime.datetime]
    src_path: Optional[str]
    dest_path: str = None

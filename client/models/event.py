"""
Represents an event that occurred in the directory.
"""
import datetime
import enum
from typing import Optional

from pydantic import BaseModel


class EventType(enum.Enum):
    ON_STARTUP = "ON_STARTUP"
    CREATED = "CREATED"
    DELETED = "DELETED"
    MODIFIED = "MODIFIED"
    DOWNLOAD = "DOWNLOAD"
    MOVED = "MOVED"
    SERVER_SYNC = "SERVER_SYNC"


class Event(BaseModel):
    type: EventType
    time: Optional[datetime.datetime]
    src_path: Optional[str]
    dest_path: str = None

"""
Represents an event that occurred in the directory.
"""
import enum

from pydantic import BaseModel


class EventType(enum.Enum):
    CREATED = "CREATED"
    DELETED = "DELETED"
    MODIFIED = "MODIFIED"
    MOVED = "MOVED"
    ROUTINE_CHECK = "ROUTINE_CHECK"


class Event(BaseModel):
    type: EventType
    src_path: str
    dest_path: str = None

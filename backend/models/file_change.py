""" A model representing a file change."""
from pydantic import BaseModel


class FileChange(BaseModel):
    offset: int
    size: int
    change: bytes

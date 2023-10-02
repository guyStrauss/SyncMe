""" A model representing a file change."""
from pydantic import BaseModel


class FileChange(BaseModel):
    """A model representing a file change."""

    offset: int
    size: int
    data: bytes

"""
This model is used to store the metadata of the file uploaded by the user.
"""
from datetime import datetime

from pydantic import BaseModel


class FileMetadata(BaseModel):
    hash: str
    user_id: str
    path: str
    last_modified: datetime
    version: int = 0

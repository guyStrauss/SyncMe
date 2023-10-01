"""
This model is used to store the metadata of the file uploaded by the user.
"""
from pydantic import BaseModel
from datetime import datetime


class FileMetadata(BaseModel):
    user_id: int
    hash: str
    path: str
    last_modified: datetime

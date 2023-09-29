"""
This model is used to store the metadata of the file uploaded by the user.
"""
from pydantic import BaseModel
from datetime import datetime


class FileMetadata(BaseModel):
    id: int
    file_name: str
    file_hash: str
    file_path: str
    last_modified: datetime

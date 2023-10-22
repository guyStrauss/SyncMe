from typing import Optional

from pydantic import BaseModel


class FilePartHash(BaseModel):
    hash: Optional[str]
    offset: int
    size: int

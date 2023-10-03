from pydantic import BaseModel


class FilePartHash(BaseModel):
    hash: str
    offset: int
    size: int

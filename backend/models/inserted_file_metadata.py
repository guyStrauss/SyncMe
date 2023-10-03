from typing import List

from backend.models.file_medadata import FileMetadata
from backend.models.file_part_hash import FilePartHash


class InsertedFileMetadata(FileMetadata):
    id: str
    hash_list: List[FilePartHash] = []

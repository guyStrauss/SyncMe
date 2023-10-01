from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileRequest(_message.Message):
    __slots__ = ["hash"]
    HASH_FIELD_NUMBER: _ClassVar[int]
    hash: str
    def __init__(self, hash: _Optional[str] = ...) -> None: ...

class File(_message.Message):
    __slots__ = ["version", "name", "hash", "data"]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    version: int
    name: str
    hash: str
    data: bytes
    def __init__(self, version: _Optional[int] = ..., name: _Optional[str] = ..., hash: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class FilePart(_message.Message):
    __slots__ = ["data", "hash", "part"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    PART_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    hash: str
    part: int
    def __init__(self, data: _Optional[bytes] = ..., hash: _Optional[str] = ..., part: _Optional[int] = ...) -> None: ...

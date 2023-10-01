from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileRequest(_message.Message):
    __slots__ = ["user_id", "hash"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    hash: str
    def __init__(self, user_id: _Optional[str] = ..., hash: _Optional[str] = ...) -> None: ...

class File(_message.Message):
    __slots__ = ["name", "data"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    data: bytes
    def __init__(self, name: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class FilePart(_message.Message):
    __slots__ = ["data", "hash", "part"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    PART_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    hash: str
    part: int
    def __init__(self, data: _Optional[bytes] = ..., hash: _Optional[str] = ..., part: _Optional[int] = ...) -> None: ...

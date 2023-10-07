from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UpdateFileName(_message.Message):
    __slots__ = ["user_id", "file_id", "new_name"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    NEW_NAME_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    file_id: str
    new_name: str
    def __init__(self, user_id: _Optional[str] = ..., file_id: _Optional[str] = ..., new_name: _Optional[str] = ...) -> None: ...

class FileList(_message.Message):
    __slots__ = ["files"]
    FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedCompositeFieldContainer[getFileAnswer]
    def __init__(self, files: _Optional[_Iterable[_Union[getFileAnswer, _Mapping]]] = ...) -> None: ...

class FileRequest(_message.Message):
    __slots__ = ["user_id", "file_id"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    file_id: str
    def __init__(self, user_id: _Optional[str] = ..., file_id: _Optional[str] = ...) -> None: ...

class CompareHash(_message.Message):
    __slots__ = ["file_id", "hash"]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    file_id: str
    hash: str
    def __init__(self, file_id: _Optional[str] = ..., hash: _Optional[str] = ...) -> None: ...

class File(_message.Message):
    __slots__ = ["user_id", "hash", "name", "data", "last_modified"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    hash: str
    name: str
    data: bytes
    last_modified: _timestamp_pb2.Timestamp
    def __init__(self, user_id: _Optional[str] = ..., hash: _Optional[str] = ..., name: _Optional[str] = ..., data: _Optional[bytes] = ..., last_modified: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FilePart(_message.Message):
    __slots__ = ["data", "size", "offset"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    size: int
    offset: int
    def __init__(self, data: _Optional[bytes] = ..., size: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class FileSyncRequest(_message.Message):
    __slots__ = ["user_id", "file_id", "parts", "last_modified"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    file_id: str
    parts: _containers.RepeatedCompositeFieldContainer[FilePart]
    last_modified: _timestamp_pb2.Timestamp
    def __init__(self, user_id: _Optional[str] = ..., file_id: _Optional[str] = ..., parts: _Optional[_Iterable[_Union[FilePart, _Mapping]]] = ..., last_modified: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Block(_message.Message):
    __slots__ = ["hash", "size", "offset"]
    HASH_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    hash: str
    size: int
    offset: int
    def __init__(self, hash: _Optional[str] = ..., size: _Optional[int] = ..., offset: _Optional[int] = ...) -> None: ...

class getFileAnswer(_message.Message):
    __slots__ = ["hash", "name", "file_id", "user_id", "last_modified"]
    HASH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    hash: str
    name: str
    file_id: str
    user_id: str
    last_modified: _timestamp_pb2.Timestamp
    def __init__(self, hash: _Optional[str] = ..., name: _Optional[str] = ..., file_id: _Optional[str] = ..., user_id: _Optional[str] = ..., last_modified: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

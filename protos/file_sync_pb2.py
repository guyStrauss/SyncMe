# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: file_sync.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x66ile_sync.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"D\n\x0eUpdateFileName\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0f\n\x07\x66ile_id\x18\x02 \x01(\t\x12\x10\n\x08new_name\x18\x03 \x01(\t\"\'\n\x08\x46ileList\x12\x1b\n\x05\x66iles\x18\x01 \x03(\x0b\x32\x0c.FileRequest\"/\n\x0b\x46ileRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0f\n\x07\x66ile_id\x18\x02 \x01(\t\",\n\x0b\x43ompareHash\x12\x0f\n\x07\x66ile_id\x18\x01 \x01(\t\x12\x0c\n\x04hash\x18\x02 \x01(\t\"t\n\x04\x46ile\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0c\n\x04hash\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x04 \x01(\x0c\x12\x31\n\rlast_modified\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"6\n\x08\x46ilePart\x12\x0c\n\x04\x64\x61ta\x18\x03 \x01(\x0c\x12\x0c\n\x04size\x18\x04 \x01(\x05\x12\x0e\n\x06offset\x18\x05 \x01(\x05\"\x80\x01\n\x0f\x46ileSyncRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0f\n\x07\x66ile_id\x18\x02 \x01(\t\x12\x18\n\x05parts\x18\x03 \x03(\x0b\x32\t.FilePart\x12\x31\n\rlast_modified\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"3\n\x05\x42lock\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x0c\n\x04size\x18\x02 \x01(\x05\x12\x0e\n\x06offset\x18\x03 \x01(\x05\x32\x85\x04\n\x08\x46ileSync\x12=\n\x0f\x64oes_file_exist\x12\x0c.FileRequest\x1a\x1a.google.protobuf.BoolValue\"\x00\x12=\n\tsync_file\x12\x10.FileSyncRequest\x1a\x1c.google.protobuf.StringValue\"\x00\x12;\n\rcheck_version\x12\x0c.CompareHash\x1a\x1a.google.protobuf.BoolValue\"\x00\x12!\n\x08get_file\x12\x0c.FileRequest\x1a\x05.File\"\x00\x12\x34\n\x0bupload_file\x12\x05.File\x1a\x1c.google.protobuf.StringValue\"\x00\x12\x39\n\x0b\x64\x65lete_file\x12\x0c.FileRequest\x1a\x1a.google.protobuf.BoolValue\"\x00\x12+\n\x0fget_file_hashes\x12\x0c.FileRequest\x1a\x06.Block\"\x00\x30\x01\x12:\n\rget_file_list\x12\x1c.google.protobuf.StringValue\x1a\t.FileList\"\x00\x12\x41\n\x10update_file_name\x12\x0f.UpdateFileName\x1a\x1a.google.protobuf.BoolValue\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'file_sync_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_UPDATEFILENAME']._serialized_start=84
  _globals['_UPDATEFILENAME']._serialized_end=152
  _globals['_FILELIST']._serialized_start=154
  _globals['_FILELIST']._serialized_end=193
  _globals['_FILEREQUEST']._serialized_start=195
  _globals['_FILEREQUEST']._serialized_end=242
  _globals['_COMPAREHASH']._serialized_start=244
  _globals['_COMPAREHASH']._serialized_end=288
  _globals['_FILE']._serialized_start=290
  _globals['_FILE']._serialized_end=406
  _globals['_FILEPART']._serialized_start=408
  _globals['_FILEPART']._serialized_end=462
  _globals['_FILESYNCREQUEST']._serialized_start=465
  _globals['_FILESYNCREQUEST']._serialized_end=593
  _globals['_BLOCK']._serialized_start=595
  _globals['_BLOCK']._serialized_end=646
  _globals['_FILESYNC']._serialized_start=649
  _globals['_FILESYNC']._serialized_end=1166
# @@protoc_insertion_point(module_scope)

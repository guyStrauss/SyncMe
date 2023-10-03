import hashlib
import random
import unittest

from google.protobuf.timestamp_pb2 import Timestamp

from backend.databases.filesystem_database import BLOCK_SIZE
from backend.file_sync_servicer import FileSyncServicer
from backend.tests.base.metadata_base_test import MetadataBaseTest
from backend.tests.base.storage_base_test import StorageBaseTest
from backend.tests.constants import USER_ID, STORAGE_DIRECTORY, METADATA_DATABASE_NAME, MEGA_BYTE
from protos import file_sync_pb2


class ServicerTests(MetadataBaseTest, StorageBaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stub = FileSyncServicer(METADATA_DATABASE_NAME, STORAGE_DIRECTORY)

    def test_upload_file(self):
        file = self.__generate_random_file()
        response = self.stub.upload_file(file, context=None)
        self.assertIsNotNone(response)

    def test_get_file(self):
        file = self.__generate_random_file()
        inserted_id = self.stub.upload_file(file, context=None)
        response = self.stub.get_file(file_sync_pb2.FileRequest(file_id=inserted_id, user_id=USER_ID), context=None)
        self.assertEqual(response.data, file.data)
        self.assertEqual(response.hash, file.hash)
        self.assertEqual(response.name, file.name)
        self.assertEqual(response.user_id, file.user_id)
        self.assertEqual(response.last_modified, file.last_modified)

    def test_does_file_exist(self):
        file = self.__generate_random_file()
        inserted_id = self.stub.upload_file(file, context=None)
        response = self.stub.does_file_exist(file_sync_pb2.FileRequest(file_id=inserted_id, user_id=USER_ID),
                                             context=None)
        self.assertTrue(response)

    def test_file_doesnt_exist(self):
        response = self.stub.does_file_exist(file_sync_pb2.FileRequest(file_id="0" * 24, user_id=USER_ID),
                                             context=None)
        self.assertFalse(response)

    def test_check_version(self):
        file = self.__generate_random_file()
        inserted_id = self.stub.upload_file(file, context=None)
        response = self.stub.check_version(file_sync_pb2.CompareHash(hash=file.hash, file_id=inserted_id), context=None)
        self.assertTrue(response)

    def test_check_version_doesnt_exist(self):
        response = self.stub.check_version(file_sync_pb2.CompareHash(hash="", file_id="0" * 24), context=None)
        self.assertFalse(response)

    def test_delete_file(self):
        file = self.__generate_random_file()
        inserted_id = self.stub.upload_file(file, context=None)
        response = self.stub.delete_file(file_sync_pb2.FileRequest(file_id=inserted_id, user_id=USER_ID), context=None)
        self.assertTrue(response)

    def test_delete_file_doesnt_exist(self):
        response = self.stub.delete_file(file_sync_pb2.FileRequest(file_id="0" * 24, user_id=USER_ID), context=None)
        self.assertFalse(response)

    def test_get_files(self):
        files = [self.__generate_random_file() for _ in range(10)]
        inserted_ids = [self.stub.upload_file(file, context=None) for file in files]
        response = self.stub.get_file_list(file_sync_pb2.FileRequest(user_id=USER_ID), context=None)
        self.assertEqual(len(response.files), len(files))
        for file in response.files:
            self.assertIn(file.file_id, inserted_ids)

    def test_sync_file(self):
        file = self.__generate_random_file()
        inserted_id = self.stub.upload_file(file, context=None)
        changes = []
        for _ in range(10):
            changes.append(file_sync_pb2.FilePart(offset=random.randrange(0, len(file.data)),
                                                  data=self.__generate_random_file(size=1024).data, size=1024))
        response = self.stub.sync_file(file_sync_pb2.FileSyncRequest(file_id=inserted_id, user_id=USER_ID,
                                                                     parts=changes), context=None)
        self.assertTrue(response)
        for change in changes:
            file.data = file.data[:change.offset] + change.data + file.data[change.offset + len(change.data):]
        new_hash = hashlib.sha256(file.data).hexdigest()
        new_file_info = self.stub.get_file(file_sync_pb2.FileRequest(file_id=inserted_id, user_id=USER_ID),
                                           context=None)
        self.assertEqual(new_hash, new_file_info.hash)
        self.assertEqual(file.data, new_file_info.data)
        file_hashes = [block.hash for block in
                       self.stub.get_file_hashes(file_sync_pb2.FileRequest(file_id=inserted_id, user_id=USER_ID),
                                                 context=None)]
        calculated_file_hashes = []
        for i in range(0, len(new_file_info.data), BLOCK_SIZE):
            calculated_file_hashes.append(
                hashlib.sha256(new_file_info.data[i:i + BLOCK_SIZE]).hexdigest())
        self.assertEqual(file_hashes, calculated_file_hashes)

    def __generate_random_file(self, size: int = 5 * MEGA_BYTE) -> [bytes, str]:
        file_data, file_hash = super()._generate_random_file(size)
        file_name = str(random.randrange(0, 1000000))
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        timestamp.nanos = 0
        file = file_sync_pb2.File(name=file_name, data=file_data, hash=file_hash,
                                  user_id=USER_ID, last_modified=timestamp)

        return file


if __name__ == '__main__':
    unittest.main()

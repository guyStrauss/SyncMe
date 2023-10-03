import random
import unittest

from google.protobuf.timestamp_pb2 import Timestamp

from backend.databases.filesystem_database import FILENAME
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

    def test_get_files(self):
        files = [self.__generate_random_file() for _ in range(10)]
        inserted_ids = [self.stub.upload_file(file, context=None) for file in files]
        response = self.stub.get_file_list(file_sync_pb2.FileRequest(user_id=USER_ID), context=None)
        self.assertEqual(len(response.files), len(files))
        for file in response.files:
            self.assertIn(file.file_id, inserted_ids)

    def __generate_random_file(self, size: int = 5 * MEGA_BYTE) -> [bytes, str]:
        file_data, file_hash = super()._generate_random_file(size)
        file_name = FILENAME + str(random.randrange(0, 1000000))
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        timestamp.nanos = 0
        file = file_sync_pb2.File(name=file_name, data=file_data, hash=file_hash,
                                  user_id=USER_ID, last_modified=timestamp)

        return file


if __name__ == '__main__':
    unittest.main()

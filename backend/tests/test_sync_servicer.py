import hashlib
import unittest
from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp

from backend.databases.filesystem_database import FILENAME
from backend.file_sync_servicer import FileSyncServicer
from backend.tests.base.metadata_base_test import MetadataBaseTest
from backend.tests.base.storage_base_test import StorageBaseTest
from backend.tests.constants import USER_ID, STORAGE_DIRECTORY, METADATA_DATABASE_NAME
from protos import file_sync_pb2


class ServicerTests(MetadataBaseTest, StorageBaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stub = FileSyncServicer(METADATA_DATABASE_NAME, STORAGE_DIRECTORY)

    def test_upload_file(self):
        file_data, file_hash = self._generate_random_file()
        now = datetime.now()
        timestamp = Timestamp()
        timestamp.FromDatetime(now)
        file = file_sync_pb2.File(name="test.txt", data=file_data, hash=hashlib.sha256(file_data).hexdigest(),
                                  user_id=USER_ID, last_modified=timestamp)
        response = self.stub.upload_file(file, context=None)
        self.assertIsNotNone(response)

    def test_get_file(self):
        file_data, file_hash = self._generate_random_file()
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        timestamp.nanos = 0
        file = file_sync_pb2.File(name=FILENAME, data=file_data, hash=file_hash,
                                  user_id=USER_ID, last_modified=timestamp)
        inserted_id = self.stub.upload_file(file, context=None)
        self.assertIsNotNone(inserted_id)
        file_request = file_sync_pb2.FileRequest(file_id=inserted_id, user_id=USER_ID)
        response = self.stub.get_file(file_request, context=None)
        self.assertEqual(response.data, file_data)
        self.assertEqual(response.hash, file_hash)
        self.assertEqual(response.name, FILENAME)
        self.assertEqual(response.user_id, USER_ID)
        self.assertEqual(response.last_modified, timestamp)


if __name__ == '__main__':
    unittest.main()

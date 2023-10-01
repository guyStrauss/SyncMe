import unittest
from datetime import datetime

from backend.databases.mongo_database import MongoDatabase
import protos.file_sync_pb2 as file_sync_pb2
from backend.models.file_medadata import FileMetadata

server = MongoDatabase("test-metadata")
FILE_HASH = "1234"
FILE_NAME = "test.txt"


class MongoTests(unittest.TestCase):
    def tearDown(self) -> None:
        server.delete_metadata(FILE_HASH)

    def setUp(self) -> None:
        server.delete_metadata(FILE_HASH)

    def test_insert(self):
        metadata = FileMetadata(path=FILE_NAME, hash=FILE_HASH, user_id=1, last_modified=datetime.now())
        server.insert_metadata(metadata)
        self.assertEqual(server.get_metadata("1234").path, FILE_NAME)

    def test_update(self):
        new_name = "this is a new name.txt"
        new_hash = "5678"
        metadata = FileMetadata(path=FILE_NAME, hash=FILE_HASH, user_id=1, last_modified=datetime.now())
        server.insert_metadata(metadata)
        metadata = FileMetadata(path=new_name, hash=new_hash, user_id=1, last_modified=datetime.now())
        server.update_metadata(metadata)
        self.assertEqual(server.get_metadata(new_hash).path, new_name)
        self.assertEqual(server.get_metadata(new_hash).hash, new_hash)


if __name__ == '__main__':
    unittest.main()

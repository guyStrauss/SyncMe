import unittest
from datetime import datetime

from backend.databases.mongo_database import MongoDatabase
import protos.file_sync_pb2 as file_sync_pb2
from backend.models.file_medadata import FileMetadata

server = MongoDatabase()


class ServicerTests(unittest.TestCase):
    def test_insert(self):
        metadata = FileMetadata(path="test.txt", hash="1234", user_id=1, last_modified=datetime.now())
        server.insert_metadata(metadata)
        self.assertEqual(server.get_metadata("1234").path, "test.txt")



if __name__ == '__main__':
    unittest.main()

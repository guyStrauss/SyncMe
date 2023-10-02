import unittest
from datetime import datetime
import pymongo

from backend.databases.exceptions.mongo_exceptions import MetadataNotFoundError
from backend.databases.mongo_database import MongoDatabase, PORT, HOST
from backend.models.file_medadata import FileMetadata

DB_NAME = "test-metadata"
FILE_HASH = "1234"
FILE_NAME = "test.txt"
UESR_ID = 1
server = MongoDatabase(DB_NAME)


class MongoTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(HOST, PORT)
        self.db = self.client[DB_NAME]
        self.collection = self.db[DB_NAME]

    def setUp(self) -> None:
        self.collection.delete_many({})

    def test_insert(self):
        metadata = FileMetadata(path=FILE_NAME, hash=FILE_HASH, user_id=UESR_ID, last_modified=datetime.now())
        inserted_id = server.insert_metadata(metadata)
        self.assertEqual(server.get_metadata(inserted_id).path, FILE_NAME)

    def test_update(self):
        new_name = "this is a new name.txt"
        new_hash = "5678"
        metadata = FileMetadata(path=FILE_NAME, hash=FILE_HASH, user_id=UESR_ID, last_modified=datetime.now())
        inserted_id = server.insert_metadata(metadata)
        metadata = FileMetadata(path=new_name, hash=new_hash, user_id=UESR_ID, last_modified=datetime.now())
        server.update_metadata(inserted_id, metadata)
        self.assertEqual(server.get_metadata(inserted_id).path, new_name)
        self.assertEqual(server.get_metadata(inserted_id).hash, new_hash)

    def test_get_all_metadata(self):
        records = [FileMetadata(path=f"{i}_{FILE_NAME}", hash=FILE_HASH, user_id=UESR_ID, last_modified=datetime.now())
                   for i
                   in range(10)]
        for record in records:
            server.insert_metadata(record)
        metadata = server.get_all_metadata(UESR_ID)
        self.assertEqual(len(metadata), 10)

    def test_delete(self):
        metadata = FileMetadata(path=FILE_NAME, hash=FILE_HASH, user_id=UESR_ID, last_modified=datetime.now())
        server.insert_metadata(metadata)
        server.delete_metadata(FILE_HASH)
        self.assertIsNone(server.get_metadata(FILE_HASH))


if __name__ == '__main__':
    unittest.main()

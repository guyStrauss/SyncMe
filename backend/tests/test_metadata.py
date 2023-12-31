import unittest
from datetime import datetime

from models.file_medadata import FileMetadata
from models.file_part_hash import FilePartHash
from tests.base.metadata_base_test import MetadataBaseTest
from tests.constants import FILE_HASH, FILE_NAME, USER_ID


class MongoTests(MetadataBaseTest):

    def test_insert(self):
        metadata = FileMetadata(path=FILE_NAME, hash=FILE_HASH, user_id=USER_ID, last_modified=datetime.now())
        inserted_id = self.server.insert_metadata(metadata)
        self.assertEqual(self.server.get_metadata(inserted_id).path, FILE_NAME)

    def test_update(self):
        new_name = "this is a new name.txt"
        new_hash = "5678"
        metadata = FileMetadata(path=FILE_NAME, hash=FILE_HASH, user_id=USER_ID, last_modified=datetime.now())
        inserted_id = self.server.insert_metadata(metadata)
        metadata = FileMetadata(path=new_name, hash=new_hash, user_id=USER_ID, last_modified=datetime.now())
        self.server.update_metadata(inserted_id, metadata)
        self.assertEqual(self.server.get_metadata(inserted_id).path, new_name)
        self.assertEqual(self.server.get_metadata(inserted_id).hash, new_hash)

    def test_get_all_metadata(self):
        records = [
            FileMetadata(path=f"{i}_{FILE_NAME}", hash=FILE_HASH, user_id=USER_ID, last_modified=datetime.now())
            for i
            in range(10)]
        for record in records:
            self.server.insert_metadata(record)
        metadata = self.server.get_all_metadata(USER_ID)
        self.assertEqual(len(metadata), 10)

    def test_update_hashes(self):
        metadata = FileMetadata(path=FILE_NAME, hash=FILE_HASH, user_id=USER_ID, last_modified=datetime.now())
        inserted_id = self.server.insert_metadata(metadata)
        hashes = [FilePartHash(hash="1234", offset=0, size=100), FilePartHash(hash="5678", offset=100, size=100)]
        response = self.server.update_file_hashes(inserted_id, hashes)
        self.assertTrue(response)
        self.assertEqual(self.server.get_metadata(inserted_id).hash_list, hashes)

    def test_get_metadata(self):
        metadata = FileMetadata(path=FILE_NAME, hash=FILE_HASH, user_id=USER_ID, last_modified=datetime.now())
        inserted_id = self.server.insert_metadata(metadata)
        self.assertEqual(self.server.get_metadata(inserted_id).hash, FILE_HASH)

    def test_delete(self):
        metadata = FileMetadata(path=FILE_NAME, hash=FILE_HASH, user_id=USER_ID, last_modified=datetime.now())
        inserted_id = self.server.insert_metadata(metadata)
        self.server.delete_metadata(inserted_id)
        self.assertIsNone(self.server.get_metadata(inserted_id))


if __name__ == '__main__':
    unittest.main()

import hashlib
import os
import random
import unittest
import zipfile

from databases.filesystem_database import FILENAME, BLOCK_SIZE
from models.file_change import FileChange
from tests.base.storage_base_test import StorageBaseTest
from tests.constants import USER_ID, MEGA_BYTE


class TestStorage(StorageBaseTest):
    def test_upload(self):
        file_data, file_hash = self._generate_random_file()
        self.storage.upload_file(USER_ID, file_hash, file_data)
        with zipfile.ZipFile(os.path.join(self.storage_location, USER_ID, file_hash + ".zip"), 'r') as zip_file:
            self.assertEqual(zip_file.read(FILENAME), file_data)

    def test_get_file(self):
        file_data, file_hash = self._generate_random_file()
        self.storage.upload_file(USER_ID, file_hash, file_data)
        self.assertEqual(self.storage.get_file(USER_ID, file_hash), file_data)

    def test_get_file_offset(self):
        file_data, file_hash = self._generate_random_file()
        self.storage.upload_file(USER_ID, file_hash, file_data)
        self.assertEqual(self.storage.get_file(USER_ID, file_hash, 100, 100), file_data[100:200])

    def test_get_file_hashes(self):
        file_data, file_hash = self._generate_random_file()
        server_hashes = [block.hash for block in self.storage.upload_file(USER_ID, file_hash, file_data)[-1]]
        hashes = []
        for i in range(0, len(file_data), BLOCK_SIZE):
            hashes.append(hashlib.sha256(file_data[i:i + BLOCK_SIZE]).hexdigest())
        self.assertEqual(server_hashes, hashes)

    def test_delete_file(self):
        file_data, file_hash = self._generate_random_file()
        os.makedirs(os.path.join(self.storage_location, USER_ID))
        with open(os.path.join(self.storage_location, USER_ID, file_hash + ".zip"), 'wb') as file:
            file.write(file_data)
        self.assertTrue(self.storage.delete_file(USER_ID, file_hash))
        self.assertFalse(os.path.exists(os.path.join(self.storage_location, USER_ID, file_hash)))

    def test_sync_file(self):
        file_data, file_hash = self._generate_random_file()
        file_id = "123456789"
        self.storage.upload_file(USER_ID, file_id, file_data)
        file_changes = []
        for _ in range(10):
            new_data = os.urandom(MEGA_BYTE // 3)
            offset = random.randrange(0, stop=len(file_data))
            file_changes.append(FileChange(offset=offset, size=len(new_data), data=new_data))
        for change in file_changes:
            file_data = file_data[:change.offset] + change.data + file_data[change.offset + len(change.data):]
        self.storage.sync_file(USER_ID, file_id, file_changes)
        self.assertEqual(self.storage.get_file(USER_ID, file_id), file_data)


if __name__ == '__main__':
    unittest.main()

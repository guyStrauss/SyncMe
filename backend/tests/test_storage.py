import hashlib
import os
import random
import unittest
import zipfile

from backend.databases.filesystem_database import FILENAME
from backend.models.file_change import FileChange
from backend.tests.base.storage_base_test import StorageBaseTest
from backend.tests.constants import USER_ID, MEGA_BYTE

USER_ID = str(USER_ID)


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

    def test_delete_file(self):
        file_data, file_hash = self._generate_random_file()
        os.makedirs(os.path.join(self.storage_location, USER_ID))
        with open(os.path.join(self.storage_location, USER_ID, file_hash + ".zip"), 'wb') as file:
            file.write(file_data)
        self.assertTrue(self.storage.delete_file(USER_ID, file_hash))
        self.assertFalse(os.path.exists(os.path.join(self.storage_location, USER_ID, file_hash)))

    def test_sync_file(self):
        file_data, file_hash = self._generate_random_file()
        self.storage.upload_file(USER_ID, file_hash, file_data)
        file_changes = []
        for _ in range(10):
            new_data = os.urandom(MEGA_BYTE // 3)
            offset = random.randrange(0, stop=len(file_data))
            file_changes.append(FileChange(offset=offset, size=len(new_data), data=new_data))
        for change in file_changes:
            file_data = file_data[:change.offset] + change.data + file_data[change.offset + len(change.data):]
        self.storage.sync_file(USER_ID, file_hash, file_changes)
        new_file_hash = hashlib.sha256(file_data).hexdigest()
        self.assertEqual(self.storage.get_file(USER_ID, new_file_hash), file_data)


if __name__ == '__main__':
    unittest.main()

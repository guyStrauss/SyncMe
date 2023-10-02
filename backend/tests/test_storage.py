import hashlib
import os
import random
import unittest
import shutil
from backend.databases.filesystem_database import FilesystemDatabase
from backend.models.file_change import FileChange

DIRECTORY = "storage_test"
MEGA_BYTE = 1024 * 1024
USER_ID = "1"


class TestStorage(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = FilesystemDatabase(DIRECTORY)

    def setUp(self) -> None:
        for file in os.listdir(DIRECTORY):
            shutil.rmtree(os.path.join(DIRECTORY, file))

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(DIRECTORY)

    def test_upload(self):
        file_data, file_hash = self._generate_random_file()
        self.storage.upload_file(USER_ID, file_hash, file_data)
        with open(os.path.join(DIRECTORY, USER_ID, file_hash), 'rb') as file:
            self.assertEqual(file.read(), file_data)

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
        os.makedirs(os.path.join(DIRECTORY, USER_ID))
        with open(os.path.join(DIRECTORY, USER_ID, file_hash), 'wb') as file:
            file.write(file_data)
        self.assertTrue(self.storage.delete_file(USER_ID, file_hash))
        self.assertFalse(os.path.exists(os.path.join(DIRECTORY, USER_ID, file_hash)))

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

    def _generate_random_file(self, size: int = 5 * MEGA_BYTE) -> [bytes, str]:
        data = os.urandom(size)
        data_hash = hashlib.sha256(data).hexdigest()
        return os.urandom(size), data_hash


if __name__ == '__main__':
    unittest.main()

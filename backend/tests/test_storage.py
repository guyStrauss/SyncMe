import os
import unittest
import shutil
from backend.databases.filesystem_database import FilesystemDatabase

DIRECTORY = "storage_test"
MEGA_BYTE = 1024 * 1024
USER_ID = "1"


class TestStorage(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = FilesystemDatabase(DIRECTORY)

    def setUp(self) -> None:
        for file in os.listdir(DIRECTORY):
            os.rmdir(os.path.join(DIRECTORY, file))

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(DIRECTORY)

    def test_upload(self):
        file_data = os.urandom(5 * MEGA_BYTE)
        self.storage.upload_file(USER_ID, "test.txt", file_data)
        with open(os.path.join(DIRECTORY, USER_ID, "test.txt"), 'rb') as file:
            self.assertEqual(file.read(), file_data)


if __name__ == '__main__':
    unittest.main()

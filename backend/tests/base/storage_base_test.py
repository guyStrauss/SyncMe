import hashlib
import os
import shutil
import unittest

from databases.filesystem_database import FilesystemDatabase
from tests.constants import STORAGE_DIRECTORY, MEGA_BYTE


class StorageBaseTest(unittest.TestCase):
    storage_location = STORAGE_DIRECTORY

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = FilesystemDatabase(self.storage_location)

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            shutil.rmtree(cls.storage_location)
        except FileNotFoundError:
            pass

    @staticmethod
    def _generate_random_file(size: int = 5 * MEGA_BYTE) -> [bytes, str]:
        data = os.urandom(size)
        data_hash = hashlib.sha256(data).hexdigest()
        return data, data_hash

    def setUp(self) -> None:
        for file in os.listdir(self.storage_location):
            shutil.rmtree(os.path.join(self.storage_location, file))

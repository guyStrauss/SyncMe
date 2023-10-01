"""
Implements the storage database interface, using the filesystem as the storage.
"""
import os
from typing import List

from backend.databases.base.storage_database import StorageDatabase
from backend.models.file_change import FileChange


class FilesystemDatabase(StorageDatabase):
    def __init__(self, root_path: str):
        """
        Initialize the database.
        :param root_path: The root path of the files.
        """
        self.root_path = root_path

    def get_file(self, user_id: str, file_id: str, file_offset: int = None, block_size: int = None) -> bytes:
        """
        Get the file from the storage.
        :param user_id: id of the user.
        :param file_offset: The offset of the file.
        :param block_size: The size of the block. For the offset
        :param file_id: The hash of the file.
        :return: The file.
        :rtype: bytes
        """
        file_path = self._get_file_path(user_id, file_id)
        with open(file_path, 'rb') as file:
            if file_offset:
                file.seek(file_offset)
                return file.read(block_size)
            return file.read()

    def upload_file(self, user_id: str, file_id: str, file: bytes) -> bool:
        """
        Upload the file to the storage.
        :param user_id: id of the user.
        :param file_id: The hash of the file.
        :param file: The file.
        :return: True if the file was uploaded successfully, False otherwise.
        :rtype: bool
        """
        user_path = os.path.join(self.root_path, user_id)
        file_path = self._get_file_path(user_id, file_id)
        if not os.path.exists(user_path):
            os.makedirs(user_path)
        with open(file_path, 'wb') as file_descriptor:
            file_descriptor.write(file)
        return True

    def delete_file(self, user_id: str, file_id: str) -> bool:
        """
        Delete the file from the storage.
        :param user_id: id of the user.
        :param file_id: The id of the file.
        :return: True if the file was deleted successfully, False otherwise.
        :rtype: bool
        """
        file_path = self._get_file_path(user_id, file_id)
        try:
            os.remove(file_path)
            return True
        except FileNotFoundError:
            return False

    def sync_file(self, user_id: str, file_id: str, changes: List[FileChange]) -> bool:
        """
        Sync the file to the storage.
        :param user_id: id of the user.
        :param file_id: The id of the file
        :param changes: The changes of the file.
        :return: True if the file was synced successfully, False otherwise.
        :rtype: bool
        """
        file_path = self._get_file_path(user_id, file_id)
        with open(file_path, 'rb+') as file:
            for change in changes:
                file.seek(change.offset)
                file.write(change.data)
        return True

    def _get_file_path(self, user_id: str, file_id: str):
        """
        Get the path of the file.
        :param user_id:
        :param file_id:
        :return:
        """
        return os.path.join(self.root_path, user_id, file_id)

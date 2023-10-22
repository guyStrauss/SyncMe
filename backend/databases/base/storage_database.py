"""
This Object will describe the interface for the storage database.
"""
from typing import List

from models.file_change import FileChange


class StorageDatabase(object):
    def get_file(self, user_id: str, file_id: str, file_parts: int) -> bytes:
        """
        Get the file from the storage.
        :param user_id: id of the user.
        :param file_parts: The offset of the file.
        :param block_size: The size of the block. For the offset
        :param file_id: The hash of the file.
        :return: The file.
        :rtype: bytes
        """
        raise NotImplementedError("This method is not implemented yet.")

    def upload_file(self, user_id: str, file_id: str, file: bytes) -> bool:
        """
        Upload the file to the storage.
        :param user_id: id of the user.
        :param file_id: The hash of the file.
        :param file: The file.
        :return: True if the file was uploaded successfully, False otherwise.
        :rtype: bool
        """
        raise NotImplementedError("This method is not implemented yet.")

    def delete_file(self, user_id: str, file_id: str) -> bool:
        """
        Delete the file from the storage.
        :param user_id: id of the user.
        :param file_id: The id of the file.
        :return: True if the file was deleted successfully, False otherwise.
        :rtype: bool
        """
        raise NotImplementedError("This method is not implemented yet.")

    def sync_file(self, user_id: str, file_id: str, changes: List[FileChange]) -> bool:
        """
        Sync the file to the storage.
        :param user_id: id of the user.
        :param file_id: The id of the file.
        :param changes: The changes of the file.
        :return: True if the file was synced successfully, False otherwise.
        :rtype: bool
        """
        raise NotImplementedError("This method is not implemented yet.")

    def calculate_hash(self, user_id: str, file_id: str) -> str:
        """
        Calculate the hash of the file.
        :param user_id: id of the user.
        :param file_id: The id of the file.
        :return: The hash of the file.
        :rtype: str
        """
        raise NotImplementedError("This method is not implemented yet.")

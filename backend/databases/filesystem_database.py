"""
Implements the storage database interface, using the filesystem as the storage.
"""
import hashlib
import logging
import os
import zipfile
from io import BytesIO
from typing import List

from databases.base.storage_database import StorageDatabase
from models.file_change import FileChange
from models.file_part_hash import FilePartHash

FILENAME = "file"
FILE_EXTENSION = ".zip"
MEGA_BYTE = 1024 * 1024
BLOCK_SIZE = MEGA_BYTE // 4


class FilesystemDatabase(StorageDatabase):
    def __init__(self, root_path: str):
        """
        Initialize the database.
        :param root_path: The root path of the files.
        """
        self.root_path = root_path
        self.zip_compress_level = zipfile.ZIP_DEFLATED
        if not os.path.exists(root_path):
            os.makedirs(root_path)

    def get_file(self, user_id: str, file_id: str, file_parts: FilePartHash = None) -> bytes:
        """
        Get the file from the storage.
        :param user_id: id of the user.
        :param file_parts: The offset of the file.
        :param block_size: The size of the block. For the offset
        :param file_id: The hash of the file.
        :return: The file.
        :rtype: bytes
        """
        file_path = self.__get_file_path(user_id, file_id)
        return self.__read_file_from_disk(file_path, file_parts)

    def upload_file(self, user_id: str, file_id: str, file: bytes) -> List[FilePartHash]:
        """
        Upload the file to the storage.
        :param user_id: id of the user.
        :param file_id: The hash of the file.
        :param file: The file.
        :return: True if the file was uploaded successfully, False otherwise.
        :rtype: bool
        """
        user_path = os.path.join(self.root_path, str(user_id))
        file_path = self.__get_file_path(user_id, file_id)
        if not os.path.exists(user_path):
            os.makedirs(user_path)
        return self.__write_file_to_disk(file_path, file)

    def delete_file(self, user_id: str, file_id: str) -> bool:
        """
        Delete the file from the storage.
        :param user_id: id of the user.
        :param file_id: The id of the file.
        :return: True if the file was deleted successfully, False otherwise.
        :rtype: bool
        """
        file_path = self.__get_file_path(user_id, file_id)
        logging.info(f"Deleting file: {file_path}")
        try:
            os.remove(file_path)
            return True
        except FileNotFoundError:
            return False

    def sync_file(self, user_id: str, file_id: str, changes: List[FileChange]) -> List[FilePartHash]:
        """
        Sync the file to the storage.
        :param user_id: id of the user.
        :param file_id: The id of the file
        :param changes: The changes of the file.
        :return: True if the file was synced successfully, False otherwise.
        :rtype: bool
        """
        return self.__write_changes(user_id, file_id, changes)

    def calculate_hash(self, user_id: str, file_id: str) -> str:
        """
        Calculate the hash of the file.
        :param user_id: id of the user.
        :param file_id: The id of the file.
        :return: The hash of the file.
        :rtype: str
        """
        return hashlib.sha256(self.__read_file_from_disk(self.__get_file_path(user_id, file_id))).hexdigest()

    def __get_file_path(self, user_id: str, file_id: str):
        """
        Get the path of the file.
        :param user_id:
        :param file_id:
        :return:
        """
        return os.path.join(self.root_path, user_id, file_id + FILE_EXTENSION)

    def __read_file_from_disk(self, file_path: str, file_parts) -> bytes | List[bytes]:
        """
        Read the file from the disk.
        :param file_path: The path of the file.
        :return: The file.
        :rtype: bytes
        """
        logging.debug(f"Reading file from disk: {file_path}")
        with zipfile.ZipFile(file_path, 'r', self.zip_compress_level) as zip_file:
            if file_parts is not None:
                with zip_file.open(FILENAME) as file:
                    data = []
                    for part in file_parts:
                        file.seek(part.offset)
                        data.append(file.read(part.size))
                    return data
            return zip_file.read(FILENAME)

    def __write_file_to_disk(self, file_path: str, file: bytes) -> [str, List[FilePartHash]]:
        """
        Write the file to the disk, and calculate the hash of the file.
        :param file_path: The path of the file.
        :param file: The file.
        """
        logging.debug(f"Writing file to disk: {file_path}")
        parts_hashes = []
        file_hash = hashlib.sha256()
        for i in range(0, len(file), BLOCK_SIZE):
            part_data = file[i:i + BLOCK_SIZE]
            file_hash.update(part_data)
            parts_hashes.append(FilePartHash(hash=hashlib.sha256(part_data).hexdigest(), offset=i, size=len(part_data)))
        with zipfile.ZipFile(file_path, 'w', self.zip_compress_level) as zip_file:
            zip_file.writestr(FILENAME, file)
        return file_hash.hexdigest(), parts_hashes

    def __write_changes(self, user_id: str, file_id: str, changes: List[FileChange]):
        """
        context manager for opening a file. after the context is closed, the file is zipped and renamed. according to
        the new hash.
        :param user_id: id of the user.
        :param file_id: The id of the file.
        :return: An object like file.
        """
        logging.debug(f"Opening file: {file_id}")
        file_path = self.__get_file_path(user_id, file_id)
        bytes_io = BytesIO()

        with zipfile.ZipFile(file_path, "r", self.zip_compress_level) as read_zip_file:
            bytes_io.write(read_zip_file.read(FILENAME))
        for change in changes:
            bytes_io.seek(change.offset)
            bytes_io.write(change.data)
            if change.size < BLOCK_SIZE:
                logging.debug("Change size is smaller than block size, probably end of file")
                bytes_io.seek(change.offset + change.size)
                bytes_io.truncate()

        return self.__write_file_to_disk(file_path, bytes_io.getvalue())

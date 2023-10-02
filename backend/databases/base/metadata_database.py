"""
This class will be responsible for the database metadata store and the interface for
"""
from bson import ObjectId

from backend.models.file_medadata import FileMetadata


class MetadataDatabase(object):
    def insert_metadata(self, metadata: FileMetadata) -> str:
        """
        Insert the metadata into the database.
        :param metadata: The metadata of the file.
        :return: The id of the file.
        :rtype: str
        """
        raise NotImplementedError("This method is not implemented yet.")

    def get_metadata(self, file_hash: str) -> FileMetadata:
        """
        Get the metadata of the file.
        :param file_hash: The hash of the file.
        :return: The metadata of the file.
        :rtype: FileMetadata
        """
        raise NotImplementedError("This method is not implemented yet.")

    def update_metadata(self, file_id: str, metadata: FileMetadata) -> bool:
        """
        Update the metadata of the file.
        :param file_id: The id of the file.
        :param metadata: The metadata of the file.
        :return: The id of the file.
        :rtype: bool
        """
        raise NotImplementedError("This method is not implemented yet.")

    def delete_metadata(self, file_hash: str) -> bool:
        """
        Delete the metadata of the file.
        :param file_hash: The hash of the file.
        :return: The id of the file.
        :rtype: bool
        """
        raise NotImplementedError("This method is not implemented yet.")

    def get_all_metadata(self, user_id: int):
        """
        Get all the metadata of the files.
        :param user_id: The id of the user.
        :return: The metadata of the files.
        :rtype: list[FileMetadata]
        """
        raise NotImplementedError("This method is not implemented yet.")

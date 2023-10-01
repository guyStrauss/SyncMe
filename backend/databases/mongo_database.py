"""
Specific implementation of the database interface for MongoDB.
"""
import logging
from pymongo import MongoClient
from backend.databases.base.metadata_database import MetadataDatabase
from backend.models.file_medadata import FileMetadata

logger = logging.getLogger(__name__)


class MongoDatabase(MetadataDatabase):
    def __init__(self, collection_name: str = "metadata"):
        """
        Initialize the database.
        """
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[collection_name]
        self.collection = self.db[collection_name]
        logger.info("Database initialized.")

    def insert_metadata(self, metadata: FileMetadata) -> str:
        """
        Insert the metadata into the database.
        :param metadata: The metadata of the file.
        :return: The id of the file.
        :rtype: str
        """
        logger.info("Inserting metadata into the database.")
        # Override the id with the hash of the file.
        return self.collection.insert_one(metadata.model_dump()).inserted_id

    def get_metadata(self, file_hash: str) -> FileMetadata:
        """
        Get the metadata of the file.
        :param file_hash: The hash of the file.
        :return: The metadata of the file.
        :rtype: FileMetadata
        """
        logger.info("Getting metadata from the database.")
        return FileMetadata(**self.collection.find_one({"hash": file_hash}))

    def update_metadata(self, metadata: FileMetadata) -> bool:
        """
        Update the metadata of the file.
        :param metadata: The metadata of the file.
        :return: The id of the file.
        :rtype: bool
        """
        logger.info("Updating metadata in the database.")
        try:
            self.delete_metadata(metadata.hash)
            self.insert_metadata(metadata)
        except Exception as e:
            logger.error("Error while updating the metadata: {}".format(e))
            return False
        return True

    def delete_metadata(self, file_hash: str) -> bool:
        """
        Delete the metadata of the file.
        :param file_id: The hash of the file.
        :return: The id of the file.
        :rtype: bool
        """
        logger.info("Deleting metadata from the database.")
        return self.collection.delete_one({"_id": file_hash}).deleted_count > 0

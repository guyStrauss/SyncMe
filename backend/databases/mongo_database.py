"""
Specific implementation of the database interface for MongoDB.
"""
import logging
from pymongo import MongoClient
from backend.databases.base.metadata_database import MetadataDatabase
from backend.models.file_medadata import FileMetadata

logger = logging.getLogger(__name__)


class MongoDatabase(MetadataDatabase):
    def __init__(self):
        """
        Initialize the database.
        """
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['metadata']
        self.collection = self.db['metadata']
        logger.info("Database initialized.")

    def insert_metadata(self, metadata: FileMetadata) -> str:
        """
        Insert the metadata into the database.
        :param metadata: The metadata of the file.
        :return: The id of the file.
        :rtype: str
        """
        logger.info("Inserting metadata into the database.")
        return self.collection.insert_one(metadata.model_dump()).inserted_id

    def get_metadata(self, file_hash: str) -> FileMetadata:
        """
        Get the metadata of the file.
        :param file_hash: The hash of the file.
        :return: The metadata of the file.
        :rtype: FileMetadata
        """
        logger.info("Getting metadata from the database.")
        return FileMetadata(**self.collection.find_one({"file_hash": file_hash}))

    def update_metadata(self, metadata: FileMetadata) -> bool:
        """
        Update the metadata of the file.
        :param metadata: The metadata of the file.
        :return: The id of the file.
        :rtype: bool
        """
        logger.info("Updating metadata in the database.")
        return self.collection.update_one({"file_hash": metadata.file_hash},
                                          {"$set": metadata.model_dump()}).modified_count > 0

    def delete_metadata(self, file_id: str) -> bool:
        """
        Delete the metadata of the file.
        :param file_id: The hash of the file.
        :return: The id of the file.
        :rtype: bool
        """
        logger.info("Deleting metadata from the database.")
        return self.collection.delete_one({"file_id": file_id}).deleted_count > 0

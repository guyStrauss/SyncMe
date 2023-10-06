"""
Specific implementation of the database interface for MongoDB.
"""
import logging
import os
from typing import List

from bson import ObjectId
from pymongo import MongoClient

from databases.base.metadata_database import MetadataDatabase
from models.file_medadata import FileMetadata
from models.file_part_hash import FilePartHash
from models.inserted_file_metadata import InsertedFileMetadata

HOST = os.environ["MONGO_URI"] if "MONGO_URI" in os.environ else "mongodb://localhost:27017"

logger = logging.getLogger(__name__)


class MongoDatabase(MetadataDatabase):
    def __init__(self, collection_name):
        """
        Initialize the database.
        """
        self.__client = MongoClient(HOST)
        self.__db = self.__client[collection_name]
        self.__collection = self.__db[collection_name]
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
        return str(self.__collection.insert_one(metadata.model_dump()).inserted_id)

    def get_metadata(self, file_id: str) -> InsertedFileMetadata | None:
        """
        Get the metadata of the file.
        :param file_id: id of the file, generated by the database.
        :return: The metadata of the file.
        :rtype: InsertedFileMetadata
        """
        logger.info("Getting metadata from the database ")
        result = self.__collection.find_one({"_id": ObjectId(file_id)})
        return InsertedFileMetadata(id=str(result["_id"]), **result) if result else None

    def update_metadata(self, file_id: str, metadata: FileMetadata) -> bool:
        """
        Update the metadata of the file.
        :param file_id: The id of the file.
        :param metadata: The metadata of the file.
        :return: The id of the file.
        :rtype: bool
        """
        logger.info("Updating metadata in the database.")
        try:
            self.__collection.update_one(
                {"_id": ObjectId(file_id)}, {"$set": metadata.model_dump(exclude={"id"})}
            )
        except Exception as e:
            logger.error("Error while updating the metadata: {}".format(e))
            return False
        return True

    def update_file_hashes(self, file_id: str, hashes_list: list[FilePartHash]) -> bool:
        """
        Update the metadata of the file.
        :param file_id: The id of the file.
        :param hashes_list: The list of hashes of the file.
        :return: The id of the file.
        :rtype: bool
        """
        logger.info("Updating metadata in the database.")
        try:
            self.__collection.update_one(
                {"_id": ObjectId(file_id)}, {"$set": {"hash_list": [part.model_dump() for part in hashes_list]}}
            )
        except Exception as e:
            logger.error("Error while updating the metadata: {}".format(e))
            return False
        return True

    def delete_metadata(self, file_id: str) -> bool:
        """
        Delete the metadata of the file.
        :param file_id: The hash of the file.
        :return: The id of the file.
        :rtype: bool
        """
        logger.info("Deleting metadata from the database.")
        return (
                self.__collection.delete_one({"_id": ObjectId(file_id)}).deleted_count > 0
        )

    def get_all_metadata(self, user_id: int) -> List[InsertedFileMetadata]:
        """
        Get all the metadata of the files.
        :param user_id: The id of the user.
        :return: The metadata of the files.
        :rtype: list[FileMetadata]
        """
        logger.info("Getting all metadata from the database.")
        return [
            InsertedFileMetadata(id=str(metadata["_id"]), **metadata)
            for metadata in self.__collection.find({"user_id": user_id})
        ]

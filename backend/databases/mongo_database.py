"""
Specific implementation of the database interface for MongoDB.
"""
import logging
from pymongo import MongoClient
from backend.databases.base.metadata_database import MetadataDatabase

logger = logging.getLogger(__name__)


class Database(MetadataDatabase):
    def __init__(self):
        """
        Initialize the database.
        """
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['metadata']
        self.collection = self.db['metadata']
        logger.info("Database initialized.")
        
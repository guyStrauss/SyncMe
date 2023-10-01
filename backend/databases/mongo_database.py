"""
Specific implementation of the database interface for MongoDB.
"""
from typing import List
from pymongo import MongoClient
from backend.databases.base.metadata_database import MetadataDatabase


class Database(MetadataDatabase):
    def __init__(self):
        """
        Initialize the database.
        """
        # Connecting to the database and collection
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['metadata']
        self.collection = self.db['metadata']


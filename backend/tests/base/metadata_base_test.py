import unittest

import pymongo

from databases.mongo_database import MongoDatabase, HOST
from tests.constants import METADATA_DATABASE_NAME


class MetadataBaseTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        client = pymongo.MongoClient(HOST)
        db = client[METADATA_DATABASE_NAME]
        self.collection = db[METADATA_DATABASE_NAME]
        self.server = MongoDatabase(METADATA_DATABASE_NAME)

    def setUp(self) -> None:
        self.collection.delete_many({})

    def tearDown(self) -> None:
        self.collection.delete_many({})

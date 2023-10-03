"""
This module is for the client database. storing files_id
"""
import tinydb


class ClientDatabase:
    def __init__(self):
        db = tinydb.TinyDB('client_db.json')
        self.table = db.table('files')

    def insert_file(self, file_id, file_name, file_hash):
        self.table.insert({'file_id': file_id, 'file_name': file_name, 'file_hash': file_hash})

    def get_file(self, file_name):
        query = tinydb.Query()
        return self.table.get(tinydb.Query().file_name == file_name)

    def delete_record(self, file_name):
        self.table.remove(tinydb.Query().file_name == file_name)

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

    def get_file_by_id(self, file_id):
        query = tinydb.Query()
        return self.table.get(tinydb.Query().file_id == file_id)

    def delete_record(self, file_name):
        self.table.remove(tinydb.Query().file_name == file_name)

    def update_file_hash(self, file_id, file_hash):
        self.table.update({'file_hash': file_hash}, tinydb.Query().file_id == file_id)

    def update_file_name(self, file_old_name, file_new_name):
        self.table.update({'file_name': file_new_name}, tinydb.Query().file_name == file_old_name)

"""
This module is for the client database. storing files_id
"""
import tinydb


class ClientDatabase:
    def __init__(self):
        db = tinydb.TinyDB('client_db.json')
        self.table = db.table('files')

    def insert_file(self, file_id, file_name, file_hash, file_timestamp, version=0):
        self.table.insert(
            {'id': file_id, 'name': file_name, 'hash': file_hash, 'timestamp': file_timestamp,
             "version": version})

    def get_file_by_name(self, file_name):
        query = tinydb.Query()
        return self.table.get(tinydb.Query().name == file_name)

    def get_file_by_id(self, file_id):
        query = tinydb.Query()
        return self.table.get(tinydb.Query().id == file_id)

    def get_file_version(self, file_id):
        return self.table.get(tinydb.Query().id == file_id)['version']

    def delete_record(self, file_name):
        self.table.remove(tinydb.Query().name == file_name)

    def update_file_hash(self, file_id, file_hash):
        self.table.update({'hash': file_hash}, tinydb.Query().id == file_id)

    def update_file_name(self, file_old_name, file_new_name):
        self.table.update({'name': file_new_name}, tinydb.Query().name == file_old_name)

    def update_file_timestamp(self, file_id, file_timestamp):
        self.table.update({'timestamp': file_timestamp}, tinydb.Query().id == file_id)

    def get_all_files(self):
        return self.table.all()

    def get_file_by_hash(self, file_hash):
        """
        Get the file by hash. used for renaming situations.
        """
        return self.table.get(tinydb.Query().hash == file_hash)

    def increment_file_version(self, file_id):
        self.table.update({'version': self.get_file_version(file_id) + 1}, tinydb.Query().id == file_id)

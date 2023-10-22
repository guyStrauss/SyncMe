"""
This module is responsible for watching the files in the directory.
"""
import datetime
import hashlib
import logging
import os
import time
from queue import Queue

from client.database import ClientDatabase
from client.models.event import Event, EventType


class DirectoryHandler:

    def __init__(self, queue: Queue, directory: str, timeout: int = 1):
        self.queue = queue
        self.directory = directory
        self.timeout = timeout
        self.local_db = ClientDatabase()
        # TODO add the files we already uploaded to the cache
        self.logger = logging.getLogger(__name__)

    def start(self):
        while True:
            time.sleep(self.timeout)
            for root, dirs, files in os.walk(self.directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not self.local_db.get_file(file_path):
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.sha256(f.read()).hexdigest()
                            if self.local_db.get_file_by_hash(file_hash):
                                self.logger.info(f"File renamed exists: {file_path}")
                                self.queue.put(Event(
                                    type=EventType.MOVED,
                                    time=datetime.datetime.now(),
                                    src_path=self.local_db.get_file_by_hash(file_hash)['file_name'],
                                    dest_path=file_path
                                ))
                                continue

                        self.logger.info(f"New file: {file_path}")
                        self.queue.put(Event(
                            type=EventType.CREATED,
                            time=datetime.datetime.now(),
                            src_path=file_path
                        ))
                    else:
                        if os.stat(file_path).st_mtime > self.local_db.get_file(file_path)['file_timestamp']:
                            self.logger.info(f"Modified file: {file_path}")
                            self.queue.put(Event(
                                type=EventType.MODIFIED,
                                time=datetime.datetime.now(),
                                src_path=file_path
                            ))
                        elif os.stat(file_path).st_mtime <= self.local_db.get_file(file_path)['file_timestamp']:
                            self.logger.info(f"Server sync file: {file_path}")
                            self.queue.put(Event(
                                type=EventType.SERVER_SYNC,
                                time=datetime.datetime.now(),
                                src_path=file_path
                            ))

                    # Checking what file got deleted
                    for file in self.local_db.get_all_files():
                        if not os.path.exists(file['file_name']):
                            self.logger.info(f"Deleted file: {file['file_name']}")
                            self.queue.put(Event(
                                type=EventType.DELETED,
                                time=datetime.datetime.now(),
                                src_path=file['file_name']
                            ))

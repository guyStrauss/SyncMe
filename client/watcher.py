"""
This module is responsible for watching the files in the directory.
"""
import datetime
import logging
import os
import time
from queue import Queue

from client.database import ClientDatabase
from client.models.event import Event, EventType


# TODO rewrite this class
class DirectoryHandler:

    def __init__(self, queue: Queue, directory: str, recursive: bool = True, timeout: int = 1):
        self.queue = queue
        self.directory = directory
        self.timeout = timeout
        self.local_db = ClientDatabase()
        # TODO add the files we already uploaded to the cache
        self.files = {}
        self.logger = logging.getLogger(__name__)

    def start(self):
        while True:
            time.sleep(self.timeout)
            for root, dirs, files in os.walk(self.directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if file_path not in self.files:
                        self.logger.info(f"New file: {file_path}")
                        self.files[file_path] = os.stat(file_path).st_mtime
                        self.queue.put(Event(
                            type=EventType.CREATED,
                            time=datetime.datetime.now(),
                            src_path=file_path
                        ))
                    else:
                        if os.stat(file_path).st_mtime != self.files[file_path]:
                            self.logger.info(f"Modified file: {file_path}")
                            self.files[file_path] = os.stat(file_path).st_mtime
                            self.queue.put(Event(
                                type=EventType.MODIFIED,
                                time=datetime.datetime.now(),
                                src_path=file_path
                            ))

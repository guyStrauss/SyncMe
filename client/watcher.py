"""
This module is responsible for watching the files in the directory.
"""
import datetime
import hashlib
import logging
import os
import time
from queue import Queue

import grpc
from google.protobuf import wrappers_pb2 as wrappers

from database import ClientDatabase
from models.event import Event, EventType
from protos import file_sync_pb2
from protos import file_sync_pb2_grpc


class DirectoryHandler:

    def __init__(self, queue: Queue, directory: str, timeout: int = 1):
        """
        :param queue: The queue to put the events in.
        :type queue: Queue
        :param directory: The directory to watch.
        :type directory: str
        :param timeout: The timeout to check for changes.
        :type timeout: int

        """
        self.queue = queue
        self.directory = directory
        self.timeout = timeout
        self.local_db = ClientDatabase()
        # Setting the grpc channel to allow large files
        options = [
            ('grpc.max_send_message_length', 1024 * 1024 * 1024),
            ('grpc.max_receive_message_length', 1024 * 1024 * 1024)]
        channel = grpc.insecure_channel('localhost:50051', options=options)
        self.stub = file_sync_pb2_grpc.FileSyncStub(channel)
        self.logger = logging.getLogger(__name__)

    def start(self):
        """
        Start the directory handler. and watch the directory changes, and monitor changes from the server
        The reason we are monitoring the server is that the server can change the file. resulting in deletion
        of the file.
        """
        while True:
            time.sleep(self.timeout)
            # Checking what file got deleted from the server before checking changes from the client
            for file in self.local_db.get_all_files():
                filename = file['name']
                try:
                    metadata = self.stub.get_file_metadata(
                        file_sync_pb2.FileRequest(file_id=file['id'], user_id="1"))
                except Exception as e:
                    metadata = None
                if not metadata:
                    os.remove(filename)
                    self.local_db.delete_record(file['name'])
                elif not os.path.exists(filename):
                    self.logger.info(f"Deleted file: {filename}")
                    self.queue.put(Event(
                        type=EventType.DELETED,
                        time=datetime.datetime.now(),
                        src_path=filename
                    ))

            # Monitoring changes from the client
            for root, dirs, files in os.walk(self.directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not self.local_db.get_file_by_name(file_path):
                        with open(file_path, 'rb') as f:
                            file_hash = hashlib.sha256(f.read()).hexdigest()
                            if self.local_db.get_file_by_hash(file_hash):
                                self.logger.info(f"File renamed exists: {file_path}")
                                self.queue.put(Event(
                                    type=EventType.MOVED,
                                    time=datetime.datetime.now(),
                                    src_path=self.local_db.get_file_by_hash(file_hash)['name'],
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
                        if os.stat(file_path).st_mtime > self.local_db.get_file_by_name(file_path)['timestamp']:
                            self.logger.info(f"Modified file: {file_path}")
                            self.queue.put(Event(
                                type=EventType.MODIFIED,
                                time=datetime.datetime.now(),
                                src_path=file_path
                            ))
                        else:
                            file_id = self.local_db.get_file_by_name(file_path)['id']
                            version = self.local_db.get_file_version(file_id)
                            if version < self.stub.get_file_metadata(
                                    file_sync_pb2.FileRequest(file_id=file_id, user_id="1")).version:
                                self.logger.info(f"Server sync file: {file_path}")
                                self.queue.put(Event(
                                    type=EventType.SERVER_SYNC,
                                    time=datetime.datetime.now(),
                                    src_path=file_path
                                ))

            file_list = self.stub.get_file_list(wrappers.StringValue(value="1"))
            for file in file_list.files:
                if not self.local_db.get_file_by_id(file.file_id):
                    self.queue.put(Event(
                        type=EventType.DOWNLOAD,
                        time=datetime.datetime.now(),
                        src_path=file.file_id
                    ))

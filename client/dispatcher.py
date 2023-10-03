"""
This module is responsible for the communication between the client and the server.
"""
import hashlib
import logging
import time
from queue import Queue

import grpc
from google.protobuf.timestamp_pb2 import Timestamp

from client.database import ClientDatabase
from client.models.event import EventType, Event
from protos import file_sync_pb2_grpc, file_sync_pb2


class RequestDispatcher:
    """
    This class is responsible for dispatching requests to the server.
    Uses queue to get requests from the client.
    """

    def __init__(self, queue: Queue):
        """
        :param queue: The queue to get requests from.
        """
        self.queue = queue
        channel = grpc.insecure_channel('localhost:50051')
        self.stub = file_sync_pb2_grpc.FileSyncStub(channel)
        self.local_db = ClientDatabase()
        self.handlers = {
            EventType.CREATED: self.file_created,
            EventType.DELETED: self.file_deleted,
            # EventType.MODIFIED: self.file_modified,
            # EventType.MOVED: self.file_moved,
            # EventType.ROUTINE_CHECK: self.routine_check
        }

    def run(self):
        """
        This function runs the dispatcher.
        run in a separate thread.
        """
        while True:
            request = self.queue.get()
            print(f"Got request: {request}")
            self.handlers[request.type](request)

    def file_created(self, event: Event):
        """
        Handle the file created event.
        """
        while True:
            try:
                file_descriptor = open(event.src_path, "rb")
                file_data = file_descriptor.read()
                file_descriptor.close()
                break
            except PermissionError:
                time.sleep(1)

        file_hash = hashlib.sha256(file_data).hexdigest()
        timestamp = Timestamp()
        timestamp.FromDatetime(event.time)
        file = file_sync_pb2.File(name=event.src_path, data=file_data, user_id="1", last_modified=timestamp,
                                  hash=file_hash)
        file_id = self.stub.upload_file(file).value
        logging.info(f"Uploaded file with id: {file_id}")
        self.local_db.insert_file(file_id, event.src_path, file_hash)

    def file_deleted(self, event: Event):
        """
        Handle the file deleted event.
        """
        file_info = self.local_db.get_file(event.src_path)
        result = self.stub.delete_file(file_sync_pb2.FileRequest(user_id="1", file_id=file_info["file_id"])).value
        if not result:
            logging.warning(f"Failed to delete file with id: {file_info['file_id']}")
            return
        self.local_db.delete_record(event.src_path)

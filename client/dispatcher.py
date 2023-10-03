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
        options = [
            ('grpc.max_send_message_length', 1024 * 1024 * 1024),
            ('grpc.max_receive_message_length', 1024 * 1024 * 1024)]
        channel = grpc.insecure_channel('localhost:50051', options=options)
        self.stub = file_sync_pb2_grpc.FileSyncStub(channel)
        self.local_db = ClientDatabase()
        self.handlers = {
            EventType.CREATED: self.file_created,
            EventType.DELETED: self.file_deleted,
            EventType.MODIFIED: self.file_modified,
            EventType.MOVED: self.file_moved,
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
            except FileNotFoundError:
                return

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
        if not file_info:
            return
        result = self.stub.delete_file(file_sync_pb2.FileRequest(user_id="1", file_id=file_info["file_id"])).value
        if not result:
            logging.warning(f"Failed to delete file with id: {file_info['file_id']}")
            return

    def file_modified(self, event: Event):
        """
        Handle the file modified event.
        """
        file_info = self.local_db.get_file(event.src_path)
        file_changes = []
        try:
            with open(event.src_path, "rb") as file:
                for file_part in self.stub.get_file_hashes(
                        file_sync_pb2.FileRequest(user_id="1", file_id=file_info["file_id"])):
                    file.seek(file_part.offset)
                    file_part_content = file.read(file_part.size)
                    if file_part.hash != hashlib.sha256(file_part_content).hexdigest():
                        file_changes.append(file_sync_pb2.FilePart(offset=file_part.offset, size=file_part.size,
                                                                   data=file_part_content))
                self.stub.sync_file(file_sync_pb2.FileSyncRequest(user_id="1", file_id=file_info["file_id"],
                                                                  parts=file_changes))
                file.seek(0)
                new_hash = hashlib.sha256(file.read()).hexdigest()
                self.local_db.update_file_hash(file_info["file_id"], new_hash)
                logging.info(f"Updated file with id: {file_info['file_id']}, new hash: {new_hash}")
        except FileNotFoundError:
            pass

    def file_moved(self, event: Event):
        """
        Handle the file moved event.
        """
        file_id = self.local_db.get_file(event.src_path)["file_id"]
        self.local_db.update_file_name(event.src_path, event.dest_path)
        self.stub.update_file_name(file_sync_pb2.UpdateFileName(user_id="1", file_id=file_id, new_name=event.dest_path))

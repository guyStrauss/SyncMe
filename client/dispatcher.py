"""
This module is responsible for the communication between the client and the server.
"""
import datetime
import hashlib
import logging
import os
import time
from queue import Queue

import grpc
from google.protobuf import wrappers_pb2 as wrappers
from google.protobuf.timestamp_pb2 import Timestamp

from client.database import ClientDatabase
from client.models.event import EventType, Event
from databases.filesystem_database import BLOCK_SIZE
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
            EventType.ON_STARTUP: self.startup,
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
        self.startup()
        while True:
            request = self.queue.get()  # type: Event
            print(f"Got request: {request}")
            self.handlers[request.type](request)

    def startup(self):
        """
        Get all the files from the server
        """
        file_list = self.stub.get_file_list(wrappers.StringValue(value="1"))
        for file in file_list:
            # TODO finish this
            file_metadata = self.stub.get_file_metadata(file_sync_pb2.FileRequest(user_id="1", file_id=file.file_id))
            if not self.local_db.get_file(file.name):
                self.local_db.insert_file(file.file_id, file.name, file.hash,
                                          datetime.datetime.fromtimestamp(file.last_modified.seconds))
                file_data = self.stub.get_file(file_sync_pb2.FileRequest(user_id="1", file_id=file.file_id)).data
                with open(file.name, "wb") as file_descriptor:
                    file_descriptor.write(file_data)
                self.local_db.update_file_timestamp(file.file_id, os.stat(file.name).st_mtime)
                logging.info(f"Downloaded file with id: {file.file_id}")

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
        self.local_db.insert_file(file_id, event.src_path, file_hash, os.stat(event.src_path).st_mtime)

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
        self.local_db.delete_record(event.src_path)

    def file_modified(self, event: Event):
        """
        Handle the file modified event.
        """
        file_info = self.local_db.get_file(event.src_path)
        file_changes = {}
        file_offset = 0
        try:
            with open(event.src_path, "rb") as file:
                for i in range(file_offset, os.stat(event.src_path).st_size, BLOCK_SIZE):
                    file.seek(i)
                    file_part_content = file.read(BLOCK_SIZE)
                    part_hash = hashlib.sha256(file_part_content).hexdigest()
                    file_changes[part_hash] = file_sync_pb2.FilePart(offset=i, size=len(file_part_content),
                                                                     data=file_part_content)
                for file_part in self.stub.get_file_hashes(
                        file_sync_pb2.FileRequest(user_id="1", file_id=file_info["file_id"])):
                    if file_part.hash in file_changes:
                        del file_changes[file_part.hash]
                # writing changes that occurred in the end of the file
                timestamp = Timestamp()
                timestamp.FromDatetime(event.time)
                self.stub.sync_file(
                    file_sync_pb2.FileSyncRequest(user_id="1", file_id=file_info["file_id"],
                                                  parts=file_changes.values(), last_modified=timestamp))

                with open(event.src_path, "rb") as file:
                    new_hash = hashlib.sha256(file.read()).hexdigest()
                self.local_db.update_file_hash(file_info["file_id"], new_hash)
                self.local_db.update_file_timestamp(file_info["file_id"], os.stat(event.src_path).st_mtime)
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

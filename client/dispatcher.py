"""
This module is responsible for the communication between the client and the server.
"""
import datetime
import hashlib
import logging
import os
import time
from itertools import zip_longest
from queue import Queue

import grpc
from google.protobuf import wrappers_pb2 as wrappers
from google.protobuf.timestamp_pb2 import Timestamp

from database import ClientDatabase
from models.event import EventType, Event
from protos import file_sync_pb2_grpc, file_sync_pb2
from protos.file_sync_pb2 import FilePart

MEGA_BYTE = 1024 * 1024
BLOCK_SIZE = MEGA_BYTE // 4


class RequestDispatcher:
    """
    This class is responsible for dispatching requests to the server.
    Uses queue to get requests from the
    """

    def __init__(self, directory: str):
        """
        :param queue: The queue to get requests from.
        """
        self.directory = directory
        options = [
            ('grpc.max_send_message_length', 1024 * 1024 * 1024),
            ('grpc.max_receive_message_length', 1024 * 1024 * 1024)]
        channel = grpc.insecure_channel('localhost:50051', options=options)
        self.stub = file_sync_pb2_grpc.FileSyncStub(channel)
        self.local_db = ClientDatabase(directory)
        os.chdir(self.directory)
        self.handlers = {
            EventType.CREATED: self.file_created,
            EventType.DELETED: self.file_deleted,
            EventType.MODIFIED: self.file_modified,
            EventType.DOWNLOAD: self.download_file,
            EventType.MOVED: self.file_moved,
            EventType.SERVER_SYNC: self.sync_file_from_server,
        }

    def startup(self):
        """
        Get all the files from the server
        """
        file_list = self.stub.get_file_list(wrappers.StringValue(value="1"))
        for file in file_list.files:
            if not self.local_db.get_file_by_id(file.file_id):
                self.download_file(Event(
                    type=EventType.DOWNLOAD,
                    time=datetime.datetime.now(),
                    src_path=file.file_id
                ))
            else:
                version = self.local_db.get_file_version(file.file_id)
                filename = self.local_db.get_file_by_id(file.file_id)["name"]
                if version > file.version:
                    self.file_modified(Event(
                        type=EventType.MODIFIED,
                        time=datetime.datetime.now(),
                        src_path=filename
                    ))
                elif version < file.version:
                    self.sync_file_from_server(Event(
                        type=EventType.SERVER_SYNC,
                        time=datetime.datetime.now(),
                        src_path=filename
                    ))

    def sync_file_from_server(self, event: Event):
        """
        Sync the file from the server. (download only the diff)
        """
        # calc the diff between the server and the client
        local_file_parts = []
        file_id = self.local_db.get_file_by_name(event.src_path)["id"]
        with open(event.src_path, "rb") as file:
            for i, block in zip_longest(range(0, os.stat(event.src_path).st_size, BLOCK_SIZE),
                                        self.stub.get_file_hashes(
                                            file_sync_pb2.FileRequest(user_id="1", file_id=file_id)),
                                        fillvalue=0):
                file.seek(i)
                file_part_content = file.read(BLOCK_SIZE)
                part_hash = hashlib.sha256(file_part_content).hexdigest()
                if part_hash != block.hash:
                    local_file_parts.append(FilePart(offset=i, size=BLOCK_SIZE, data=b""))
        # download the diff
        file = self.stub.sync_file_server(
            file_sync_pb2.SyncFileServerRequest(user_id="1", file_id=file_id, parts=local_file_parts))
        if len(file.parts) > 0:
            with open(event.src_path, "wb") as file_writer:
                for part in file.parts:
                    file_writer.seek(part.offset)
                    file_writer.write(part.data)
            # Change last modified time to the server's last modified time
            timestamp = datetime.datetime.fromtimestamp(file.last_modified.seconds).timestamp()
            self.local_db.update_file_timestamp(file_id, timestamp)
            self.local_db.increment_file_version(file_id)
            # Update the hash of the file
            with open(event.src_path, "rb") as file:
                new_hash = hashlib.sha256(file.read()).hexdigest()
            os.utime(event.src_path, (timestamp, timestamp))
            self.local_db.update_file_hash(file_id, new_hash)

    def download_file(self, event: Event):
        """
        Download the file from the server.
        """
        logging.info(f"Downloading file with id: {event.src_path}")
        file = self.stub.get_file(file_sync_pb2.FileRequest(user_id="1", file_id=event.src_path))
        # Create the directory
        os.makedirs(os.path.dirname(os.path.join(self.directory, file.name)), exist_ok=True)
        with open(os.path.join(self.directory, file.name), "wb") as file_writer:
            file_writer.write(file.data)
        timestamp = datetime.datetime.fromtimestamp(file.last_modified.seconds).timestamp()
        os.utime(os.path.join(self.directory, file.name), (timestamp, timestamp))
        self.local_db.insert_file(event.src_path, file.name, file.hash, timestamp, file.version)

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
        date_time = datetime.datetime.fromtimestamp(os.stat(event.src_path).st_mtime)
        timestamp.FromSeconds(int(date_time.timestamp()))
        file = file_sync_pb2.File(name=event.src_path, data=file_data, user_id="1", last_modified=timestamp,
                                  hash=file_hash)
        file_id = self.stub.upload_file(file).value
        logging.info(f"Uploaded file with id: {file_id}")
        self.local_db.insert_file(file_id, event.src_path, file_hash, os.stat(event.src_path).st_mtime)

    def file_deleted(self, event: Event):
        """
        Handle the file deleted event.
        """
        file_info = self.local_db.get_file_by_name(event.src_path)
        if not file_info:
            return
        result = self.stub.delete_file(file_sync_pb2.FileRequest(user_id="1", file_id=file_info["id"])).value
        if not result:
            logging.warning(f"Failed to delete file with id: {file_info['id']}")
            return
        self.local_db.delete_record(event.src_path)

    def file_modified(self, event: Event):
        """
        Handle the file modified event.
        """
        file_info = self.local_db.get_file_by_name(event.src_path)
        file_id = file_info["id"]
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
                        file_sync_pb2.FileRequest(user_id="1", file_id=file_id)):
                    if file_part.hash in file_changes:
                        del file_changes[file_part.hash]
                # writing changes that occurred in the end of the file
                timestamp = Timestamp()
                date_time = datetime.datetime.fromtimestamp(os.stat(event.src_path).st_mtime)
                timestamp.FromSeconds(int(date_time.timestamp()))
                self.stub.sync_file(
                    file_sync_pb2.FileSyncRequest(user_id="1", file_id=file_id,
                                                  parts=file_changes.values(), last_modified=timestamp))

                with open(event.src_path, "rb") as file:
                    new_hash = hashlib.sha256(file.read()).hexdigest()
                self.local_db.update_file_hash(file_id, new_hash)
                self.local_db.update_file_timestamp(file_id, os.stat(event.src_path).st_mtime)
                self.local_db.increment_file_version(file_id)
                logging.info(f"Updated file with id: {file_id}, new hash: {new_hash}")
        except FileNotFoundError:
            pass

    def file_moved(self, event: Event):
        """
        Handle the file moved event.
        """
        file_id = self.local_db.get_file_by_name(event.src_path)["id"]
        self.local_db.update_file_name(event.src_path, event.dest_path)
        self.stub.update_file_name(file_sync_pb2.UpdateFileName(user_id="1", file_id=file_id, new_name=event.dest_path))
        self.local_db.increment_file_version(file_id)

    def rename_file(self, file_id):
        old_name = self.local_db.get_file_by_id(file_id)["name"]
        new_name = self.stub.get_file_metadata(file_sync_pb2.FileRequest(user_id="1", file_id=file_id)).name
        os.rename(old_name, new_name)
        self.local_db.update_file_name(old_name, new_name)
        self.local_db.increment_file_version(file_id)




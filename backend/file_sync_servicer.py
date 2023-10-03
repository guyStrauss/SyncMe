import logging
from concurrent import futures
from datetime import datetime

import grpc
from google.protobuf.timestamp_pb2 import Timestamp

from backend.databases.filesystem_database import FilesystemDatabase
from backend.databases.mongo_database import MongoDatabase
from backend.models.file_change import FileChange
from backend.models.file_medadata import FileMetadata
from protos import file_sync_pb2_grpc, file_sync_pb2

STORAGE_DIRECTORY = "storage/"
METADATA_COLLECTION = "metadata"


class FileSyncServicer(file_sync_pb2_grpc.FileSyncServicer):
    def __init__(self, metadata: str = METADATA_COLLECTION, storage_directory: str = STORAGE_DIRECTORY, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logging.getLogger(__name__)
        self.metadata_db = MongoDatabase(metadata)
        self.storage_db = FilesystemDatabase(storage_directory)

    def get_file(self, request: file_sync_pb2.FileRequest, context):
        """
        Get the file from the storage. mostly used for downloading files. after first initial setup.
        """
        self._logger.info("get_file called")
        metadata = self.metadata_db.get_metadata(request.file_id)
        if request.user_id != metadata.user_id:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "User id does not match the file id.")
        file = self.storage_db.get_file(request.user_id, metadata.id)
        timestamp = Timestamp()
        timestamp.FromDatetime(metadata.last_modified)
        return file_sync_pb2.File(name=metadata.path, data=file, hash=metadata.hash,
                                  last_modified=timestamp,
                                  user_id=metadata.user_id)

    def check_version(self, request: file_sync_pb2.CompareHash, context):
        """
        Check if the file is the latest version.
        """
        self._logger.info("check_version called with hash: %s", request.file_id)
        metadata = self.metadata_db.get_metadata(request.file_id)
        return metadata.hash == request.hash if metadata else False

    def does_file_exist(self, request: file_sync_pb2.FileRequest, context):
        """
        Check if the file exists.
        """
        metadata = self.metadata_db.get_metadata(request.file_id)
        return metadata is not None

    def upload_file(self, request, context):
        """
        Upload the file to the storage.
        """
        self._logger.info("upload_file called with hash: %s", request.hash)
        last_modified = datetime.utcfromtimestamp(request.last_modified.seconds)
        metadata = FileMetadata(hash=request.hash, user_id=request.user_id, path=request.name,
                                last_modified=last_modified)
        inserted_id = self.metadata_db.insert_metadata(metadata)
        file_hashes = self.storage_db.upload_file(request.user_id, inserted_id, request.data)
        self.metadata_db.update_file_hashes(inserted_id, file_hashes)
        return inserted_id

    def get_file_list(self, request, context):
        """
        Get the list of files for the user.
        """
        self._logger.info("get_file_list called")
        metadata = self.metadata_db.get_all_metadata(request.user_id)
        return file_sync_pb2.FileList(
            files=[file_sync_pb2.FileRequest(user_id=metadata.user_id, file_id=metadata.id)
                   for metadata in metadata])

    def delete_file(self, request, context):
        """
        Delete the file from the storage.
        """
        self._logger.info("delete_file called")
        metadata = self.metadata_db.get_metadata(request.file_id)
        if not metadata:
            return False
        if request.user_id != metadata.user_id:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "User id does not match the file id.")
        try:
            self.metadata_db.delete_metadata(request.file_id)
            self.storage_db.delete_file(request.user_id, metadata.hash)
        except Exception as e:
            self._logger.error("Error while deleting the file: {}".format(e))
            return False
        return True

    def get_file_hashes(self, request, context):
        """
        Get the list of hashes for the user. Used for syncing. and user determines block size
        """
        self._logger.info("get_file_hashes called")
        metadata = self.metadata_db.get_metadata(request.file_id)
        if request.user_id != metadata.user_id:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "User id does not match the file id.")
        file_hashes = self.metadata_db.get_metadata(metadata.id).hash_list
        for part_file_hash in file_hashes:
            yield file_sync_pb2.Block(hash=part_file_hash.hash, offset=part_file_hash.offset, size=part_file_hash.size)

    def sync_file(self, request, context):
        """
        Sync the file to the storage.
        """
        self._logger.info("sync_file called")
        metadata = self.metadata_db.get_metadata(request.file_id)
        if request.user_id != metadata.user_id:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "User id does not match the file id.")
        changes = [FileChange(offset=part.offset, size=part.size, data=part.data) for part in request.parts]
        file_hashes = self.storage_db.sync_file(request.user_id, metadata.id, changes)
        metadata.hash = self.storage_db.calculate_hash(request.user_id, metadata.id)
        metadata.hash_list = file_hashes
        self.metadata_db.update_metadata(request.file_id, metadata)
        return True

    def update_file_name(self, request, context):
        """
        Update the file name in the database.
        """
        self._logger.info("update_file_name called")
        metadata = self.metadata_db.get_metadata(request.file_id)
        if request.user_id != metadata.user_id:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "User id does not match the file id.")
        metadata.path = request.new_name
        self.metadata_db.update_metadata(request.file_id, metadata)
        return True


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_sync_pb2_grpc.add_FileSyncServicer_to_server(FileSyncServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    serve()

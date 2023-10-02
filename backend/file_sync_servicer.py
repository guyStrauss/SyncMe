import logging
from concurrent import futures
import grpc

from backend.databases.exceptions.mongo_exceptions import MetadataNotFoundError
from backend.models.file_medadata import FileMetadata
from protos import file_sync_pb2_grpc, file_sync_pb2
from backend.databases.filesystem_database import FilesystemDatabase
from backend.databases.mongo_database import MongoDatabase


class FileSyncServicer(file_sync_pb2_grpc.FileSyncServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logging.getLogger(__name__)
        self.metadata_db = MongoDatabase()
        self.storage_db = FilesystemDatabase("/storage")

    def get_file(self, request: file_sync_pb2.FileRequest, context):
        """
        Get the file from the storage. mostly used for downloading files. after first initial setup.
        """
        self._logger.info("get_file called")
        metadata = self.metadata_db.get_metadata(request.hash)
        if request.user_id != metadata.user_id:
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "User id does not match the file id.")
        file = self.storage_db.get_file(request.user_id, request.hash)

        return file_sync_pb2.File(name=metadata.path, data=file)

    def check_version(self, request: file_sync_pb2.CompareHash, context):
        """
        Check if the file is the latest version.
        """
        self._logger.info("check_version called with hash: %s", request.hash)
        metadata = self.metadata_db.get_metadata(request.hash)
        return metadata.hash == request.hash

    def does_file_exist(self, request: file_sync_pb2.FileRequest, context):
        """
        Check if the file exists.
        """
        self._logger.info("does_file_exist called with hash: %s", request.hash)
        metadata = self.metadata_db.get_metadata(request.hash)
        return metadata is not None

    def upload_file(self, request, context):
        """
        Upload the file to the storage.
        """
        self._logger.info("upload_file called with hash: %s", request.hash)
        metadata = FileMetadata(hash=request.hash, user_id=request.user_id, path=request.name,
                                last_modified=request.last_modified)
        self.metadata_db.insert_metadata(metadata)
        self.storage_db.upload_file(request.user_id, request.hash, request.data)
        return self.storage_db.calculate_hash(request.user_id, request.hash) == request.hash


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_sync_pb2_grpc.add_FileSyncServicer_to_server(FileSyncServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    serve()

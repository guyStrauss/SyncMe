import logging
from concurrent import futures
import grpc

from protos import file_sync_pb2_grpc, file_sync_pb2
from backend.databases.filesystem_database import FilesystemDatabase
from backend.databases.mongo_database import MongoDatabase


class FileSyncServicer(file_sync_pb2_grpc.FileSyncServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logging.getLogger(__name__)
        self.metadata_db = MongoDatabase()
        self.storage_db = FilesystemDatabase("/storage")

    def GetFile(self, request: file_sync_pb2.FileRequest, context):
        self._logger.info("GetFile called")
        file_name = self.metadata_db.get_metadata(request.hash).file_name
        file = self.storage_db.get_file(request.user_id, request.hash)

        return file_sync_pb2.File(name=file_name, data=file)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_sync_pb2_grpc.add_FileSyncServicer_to_server(FileSyncServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    serve()

import logging
from concurrent import futures
import grpc

from protos import file_sync_pb2_grpc, file_sync_pb2


class FileSyncServicer(file_sync_pb2_grpc.FileSyncServicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logging.getLogger(__name__)

    def GetFile(self, request, context):
        self._logger.info("GetFile called")
        print(request.name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_sync_pb2_grpc.add_FileSyncServicer_to_server(FileSyncServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()

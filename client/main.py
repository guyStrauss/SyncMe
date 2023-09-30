"""
For now, POC for the client side of the application.
"""
import grpc
from protos import file_sync_pb2_grpc, file_sync_pb2


def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = file_sync_pb2_grpc.FileSyncStub(channel)
        stub.GetFile(file_sync_pb2.compactFile(name="test.txt", hash="1234567890"))


if __name__ == '__main__':
    main()

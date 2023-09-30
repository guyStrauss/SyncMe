# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import file_sync_pb2 as file__sync__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


class FileSyncStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.doesFileExists = channel.unary_unary(
                '/FileSync/doesFileExists',
                request_serializer=file__sync__pb2.File.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_wrappers__pb2.BoolValue.FromString,
                )
        self.SyncFile = channel.stream_stream(
                '/FileSync/SyncFile',
                request_serializer=file__sync__pb2.FilePart.SerializeToString,
                response_deserializer=file__sync__pb2.FilePart.FromString,
                )
        self.CheckVersion = channel.unary_unary(
                '/FileSync/CheckVersion',
                request_serializer=file__sync__pb2.compactFile.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_wrappers__pb2.BoolValue.FromString,
                )
        self.GetFile = channel.unary_unary(
                '/FileSync/GetFile',
                request_serializer=file__sync__pb2.File.SerializeToString,
                response_deserializer=file__sync__pb2.File.FromString,
                )
        self.UploadFile = channel.unary_unary(
                '/FileSync/UploadFile',
                request_serializer=file__sync__pb2.File.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_wrappers__pb2.BoolValue.FromString,
                )


class FileSyncServicer(object):
    """Missing associated documentation comment in .proto file."""

    def doesFileExists(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SyncFile(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckVersion(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UploadFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FileSyncServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'doesFileExists': grpc.unary_unary_rpc_method_handler(
                    servicer.doesFileExists,
                    request_deserializer=file__sync__pb2.File.FromString,
                    response_serializer=google_dot_protobuf_dot_wrappers__pb2.BoolValue.SerializeToString,
            ),
            'SyncFile': grpc.stream_stream_rpc_method_handler(
                    servicer.SyncFile,
                    request_deserializer=file__sync__pb2.FilePart.FromString,
                    response_serializer=file__sync__pb2.FilePart.SerializeToString,
            ),
            'CheckVersion': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckVersion,
                    request_deserializer=file__sync__pb2.compactFile.FromString,
                    response_serializer=google_dot_protobuf_dot_wrappers__pb2.BoolValue.SerializeToString,
            ),
            'GetFile': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFile,
                    request_deserializer=file__sync__pb2.File.FromString,
                    response_serializer=file__sync__pb2.File.SerializeToString,
            ),
            'UploadFile': grpc.unary_unary_rpc_method_handler(
                    servicer.UploadFile,
                    request_deserializer=file__sync__pb2.File.FromString,
                    response_serializer=google_dot_protobuf_dot_wrappers__pb2.BoolValue.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'FileSync', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FileSync(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def doesFileExists(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FileSync/doesFileExists',
            file__sync__pb2.File.SerializeToString,
            google_dot_protobuf_dot_wrappers__pb2.BoolValue.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SyncFile(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/FileSync/SyncFile',
            file__sync__pb2.FilePart.SerializeToString,
            file__sync__pb2.FilePart.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckVersion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FileSync/CheckVersion',
            file__sync__pb2.compactFile.SerializeToString,
            google_dot_protobuf_dot_wrappers__pb2.BoolValue.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FileSync/GetFile',
            file__sync__pb2.File.SerializeToString,
            file__sync__pb2.File.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UploadFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/FileSync/UploadFile',
            file__sync__pb2.File.SerializeToString,
            google_dot_protobuf_dot_wrappers__pb2.BoolValue.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

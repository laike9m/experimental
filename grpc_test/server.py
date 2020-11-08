import communication_pb2, communication_pb2_grpc  # noqa
from google.protobuf.empty_pb2 import Empty
import grpc
import time

from concurrent import futures


class MyServicer(communication_pb2_grpc.CommunicationServicer):
    def SendFrame(self, request: communication_pb2.Frame, context: grpc.RpcContext):
        print("get SendFrame")
        return Empty()

    def GetTargetFrame(self, request, context):
        print("get GetTargetFrame")
        data = ["foo", "bar", "baz"]
        for i in range(3):
            time.sleep(1)
            yield communication_pb2.Frame(name=data[i])


server = grpc.server(
    futures.ThreadPoolExecutor(max_workers=5),
    compression=grpc.Compression.Gzip,
)

communication_pb2_grpc.add_CommunicationServicer_to_server(
    servicer=MyServicer(), server=server
)

server.add_insecure_port(f"[::]:50051")
server.start()
print("Listening...")
server.wait_for_termination()

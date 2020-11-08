import communication_pb2, communication_pb2_grpc  # noqa
import grpc
from threading import Thread
import time


class Client:
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = communication_pb2_grpc.CommunicationStub(self.channel)

    def send_frame(self):
        self.stub.SendFrame(communication_pb2.Frame(name="foo"))

    def get_target_frame(self):
        resp = self.stub.GetTargetFrame(communication_pb2.FrameNameList(names=[]))
        for item in resp:
            print(f"Got {item}")


def main():
    client = Client()
    Thread(target=client.get_target_frame).start()
    print("Main thread ended")


if __name__ == "__main__":
    main()

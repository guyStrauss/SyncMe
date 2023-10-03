"""
This module is responsible for the communication between the client and the server.
"""
from queue import Queue

from client.models.event import EventType, Event


class RequestDispatcher:
    """
    This class is responsible for dispatching requests to the server.
    Uses queue to get requests from the client.
    """
    HANDLERS = {EventType.CREATED: None, EventType.DELETED: None, EventType.MODIFIED: None, EventType.MOVED: None, }

    def __init__(self, queue: Queue):
        """
        :param queue: The queue to get requests from.
        """
        self.queue = queue

    def run(self):
        """
        This function runs the dispatcher.
        run in a separate thread.
        """
        while True:
            request = self.queue.get()
            print(f"Got request: {request}")

    def file_created(self, event: Event):
        """
        Handle the file created event.
        """
        pass

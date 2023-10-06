"""
For now, POC for the client side of the application.
"""
import logging
import threading
from queue import Queue

from client.constants import DIRECTORY
from client.dispatcher import RequestDispatcher
from client.watcher import DirectoryHandler
from models.event import Event, EventType


def main():
    logging.basicConfig(level=logging.INFO)
    queue = Queue()
    queue.put(Event(type=EventType.STARTUP))
    event_handler = DirectoryHandler(queue, DIRECTORY)
    threads = [threading.Thread(target=RequestDispatcher(queue).run), threading.Thread(target=event_handler.start)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    if __name__ == '__main__':
        main()

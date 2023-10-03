"""
For now, POC for the client side of the application.
"""
import logging
import threading
from queue import Queue

from watchdog.observers import Observer

from client.constants import DIRECTORY
from client.dispatcher import RequestDispatcher
from client.watcher import DirectoryHandler


def main():
    logging.basicConfig(level=logging.INFO)
    queue = Queue()
    observer = Observer()
    event_handler = DirectoryHandler(queue)
    observer.schedule(event_handler, DIRECTORY, recursive=True)
    threading.Thread(target=RequestDispatcher(queue).run).start()
    threading.Thread(target=observer.start).start()


if __name__ == '__main__':
    main()

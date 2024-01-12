"""
For now, POC for the client side of the application.
"""
import logging
import sys
import threading
from queue import Queue

from constants import DIRECTORY
from dispatcher import RequestDispatcher
from watcher import DirectoryHandler


def main():
    logging.basicConfig(level=logging.INFO)
    queue = Queue()
    event_handler = DirectoryHandler(queue, sys.argv[1] if len(sys.argv) > 1 else DIRECTORY)
    event_handler.start()


if __name__ == '__main__':
    main()

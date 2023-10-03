"""
For now, POC for the client side of the application.
"""
import time

from watchdog.observers import Observer

from client.constants import DIRECTORY
from client.watcher import DirectoryHandler


def main():
    observer = Observer()
    event_handler = DirectoryHandler()
    observer.schedule(event_handler, DIRECTORY, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the observer gracefully if the user presses Ctrl+C
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()

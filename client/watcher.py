"""
This module is responsible for watching the files in the directory.
"""
import datetime
from queue import Queue

from watchdog.events import FileSystemEventHandler

from client.models.event import Event, EventType


class DirectoryHandler(FileSystemEventHandler):

    def __init__(self, queue: Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue

    def on_modified(self, event):
        if not event.is_directory:
            # This function is called when a file is modified
            print(f'File {event.src_path} has been modified')

    def on_created(self, event):
        if event.is_directory:
            return
        print(f'File {event.src_path} has been created')
        self.queue.put(Event(
            type=EventType.CREATED,
            time=datetime.datetime.now(),
            src_path=event.src_path
        ))

    def on_deleted(self, event):
        print(f'File {event.src_path} has been deleted')

    def on_moved(self, event):
        print(f'File {event.src_path} has been moved to {event.dest_path}')

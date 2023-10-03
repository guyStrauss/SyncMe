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
        if event.is_directory:
            return
        # This function is called when a file is modified
        self.queue.put(Event(
            type=EventType.MODIFIED,
            time=datetime.datetime.now(),
            src_path=event.src_path
        ))

    def on_created(self, event):
        if event.is_directory:
            return
        self.queue.put(Event(
            type=EventType.CREATED,
            time=datetime.datetime.now(),
            src_path=event.src_path
        ))

    def on_deleted(self, event):
        self.queue.put(Event(
            type=EventType.DELETED,
            time=datetime.datetime.now(),
            src_path=event.src_path
        ))

    def on_moved(self, event):
        print(f'File {event.src_path} has been moved to {event.dest_path}')
        self.queue.put(Event(
            type=EventType.MOVED,
            time=datetime.datetime.now(),
            src_path=event.src_path,
            dest_path=event.dest_path
        ))

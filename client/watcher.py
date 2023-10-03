"""
This module is responsible for watching the files in the directory.
"""

from watchdog.events import FileSystemEventHandler


class DirectoryHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            # This function is called when a file is modified
            print(f'File {event.src_path} has been modified')

    def on_created(self, event):
        if event.is_directory:
            return
        print(f'File {event.src_path} has been created')

    def on_deleted(self, event):
        print(f'File {event.src_path} has been deleted')

    def on_moved(self, event):
        print(f'File {event.src_path} has been moved to {event.dest_path}')

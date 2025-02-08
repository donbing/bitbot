from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from .log_decorator import info_log
import hashlib


def compute_hash(text):
    return hashlib.md5(text).hexdigest()


def watch_config_dir(config_dir_path, on_changed):
    event_handler = ConfigChangeHandler(on_changed)
    observer = Observer()
    observer.schedule(event_handler, config_dir_path)
    observer.start()


class ConfigChangeHandler(FileSystemEventHandler):
    def __init__(self, on_changed):
        self.on_changed = on_changed
        self.file_hashes = {}

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent):
            self.compare_content_hash(event.src_path)

    def compare_content_hash(self, src_path):
        file_content = self.get_file_content(src_path)
        if len(file_content) > 0:
            cached_hash = self.file_hashes.get(src_path)
            current_hash = compute_hash(file_content)
            self.check_file_changed(src_path, cached_hash, current_hash)

    def get_file_content(self, src_path):
        with open(src_path, 'rb') as file:
            return file.read()

    @info_log
    def check_file_changed(self, file_path, cached_hash, file_hash):
        new_change = file_path not in self.file_hashes
        file_changed = file_hash != cached_hash

        if new_change or file_changed:
            self.config_changed(file_path, file_hash)

    @info_log
    def config_changed(self, file_path, file_hash):
        self.file_hashes[file_path] = file_hash
        self.on_changed()

    def __repr__(self):
        return '<Config watcher>'

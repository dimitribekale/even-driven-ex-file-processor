import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from event_bus import event_bus, Event, EventType

class FileChangeHandler(FileSystemEventHandler):
    
    def __init__(self, processor_manager):
        self.processor_manager = processor_manager

    def on_created(self, event):
        """Called when a file is created"""
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)

            print(f"[FileMonitor] New file detected: {file_name}")

            # Emit FILE_CREATED event
            file_event = Event(
                event_type=EventType.FILE_CREATED,
                data= {
                    "file_path": file_path,
                    "file_name": file_name,
                    "file_size": os.path.getsize(file_path) if os.path.exists(file_path) else 0
                }
            )
            event_bus.publish(file_event)

            # Trigger processing
            self.processor_manager.process_file(file_path)

class FileMonitor:
    """Monitors a directory for file changes"""

    def __init__(self, watch_directory: str, processor_manager):
        self.watch_directory = watch_directory
        self.processor_manager = processor_manager
        self.observer = None

        os.makedirs(watch_directory, exist_ok=True)

    def start(self):
        """Start monitoring the directory"""
        event_handler = FileChangeHandler(self.processor_manager)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.watch_directory, recursive=False)
        self.observer.start()
        print(f"[FileMonitor] Started monitoring: {self.watch_directory}")

    def stop(self):
        """Stop monitoring"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print("[FileMonitor] Stopped monitoring")
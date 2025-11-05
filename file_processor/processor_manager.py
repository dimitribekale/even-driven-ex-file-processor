import os
from typing import List
from processors.base_processor import BaseProcessor
from processors.csv_processor import CSVProcessor
from processors.json_processor import JSONProcessor
from processors.text_processor import TextProcessor
from processors.image_processor import ImageProcessor
from event_bus import event_bus, Event, EventType

class ProcessorManager:
    """Manage all file processors"""

    def __init__(self):
        self.processors: List[BaseProcessor] = [
            CSVProcessor(),
            JSONProcessor(),
            TextProcessor(),
            ImageProcessor()
        ]
        print(f"[ProcessingManager] Initialized with {len(self.processors)} processors.")
    
    def process_file(self, file_path: str):
        """Processes a file with the appropriate processor"""
        file_name = os.path.basename(file_path)

        start_event = Event(
            event_type=EventType.FILE_PROCESSING_STARTED,
            data={"file_name": file_name, "file_path": file_path}
        )
        event_bus.publish(start_event)

        # Find the appropriate processor
        processor = self._find_processor(file_path)

        if processor:
            try:
                result = processor.process(file_path)

                if result.get("success"):
                    success_event = Event(
                        event_type=EventType.FILE_PROCESSED,
                        data={
                            "file_name": file_path,
                            "file_path": file_path,
                            "processor": processor.process_name,
                            "result": result
                        }
                    )
                    event_bus.publish(success_event)

                    # Emit a notification
                    notification_event = Event(
                        event_type=EventType.NOTIFICATION_SENT,
                        data={
                            "message": f"Successfully processed {file_name}",
                            "level": "success"
                        }
                    )
                    event_bus.publish(notification_event)
                else:
                    # Failure event
                    failure_event = Event(
                        event_type=EventType.PROCESSING_FAILED,
                        data={
                            "file_name": file_name,
                            "file_path": file_path,
                            "error": result.get("error", "Unknown error")
                        }
                    )
                    event_bus.publish(failure_event)

            except Exception as e:
                failure_event = Event(
                    event_type=EventType.PROCESSING_FAILED,
                    data={
                        "file_name": file_name,
                        "file_path": file_path,
                        "error": str(e)
                    }
                )
                event_bus.publish(failure_event)
        else:
            # No processor found
            failure_event = Event(
                event_type=EventType.PROCESSING_FAILED,
                data={
                    "file_name": file_name,
                    "file_path": file_path,
                    "error": "No processor available for this file type"
                }
            )
            event_bus.publish(failure_event)

    def _find_processor(self, file_path: str) -> BaseProcessor:
        for processor in self.processors:
            if processor.can_process(file_path):
                return processor
        return None
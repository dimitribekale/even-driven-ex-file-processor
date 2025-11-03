from typing import Callable, Dict, List, Any
from datetime import datetime
from enum import Enum
import threading

class EventType(Enum):
    """All event types in the system"""
    FILE_CREATED = "file_created"
    FILE_PROCESSING_STARTED = "file_processing_started"
    FILE_PROCESSED = "file_processed"
    PROCESSING_FAILED = "processing_failed"
    NOTIFICATION_SENT = "notification_sent"

class Event:
    """Event data structure"""
    def __init__(self, event_type: EventType, data: Dict[str, Any]):
        self.event_type = event_type
        self.data = data
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            "event_type": self.event_type.value,
            "data": self.data,
            "timestamp": self.timestamp
        }
    
class EventBus:
    """
    Central event bus using publish-subscribe pattern
    Thread-safe for concurrent event handling
    """
    def __init__(self):
        self._subscribers: Dict[EventType, List[Callable]] = {}
        self._event_history: List[Event] = []
        self._lock = threading.Lock()

    def subscribe(self, event_type: EventType, handler: Callable):
        """Subscribe a handler to an event type"""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(handler)
            print(f"[EventBus] Handler subscribed to {event_type.value}")

    def unsubscribe(self, event_type: EventType, handler: Callable):
        """Unsubscribe a handler from an event type"""
        with self._lock:
            if event_type in self._subscribers:
                self._subscribers[event_type].remove(handler)

    def publish(self, event: Event):
        """Publish an event to all subscribers"""
        with self._lock:
            self._event_history.append(event)
            print(f"[EventBus] Event published: {event.event_type.value}")

            if event.event_type in self._subscribers:
                for handler in self._subscribers[event.event_type]:
                    try:
                        # Execute handler in a separate thread to avoid blocking
                        thread = threading.Thread(target=handler, args=(event,))
                        thread.daemon = True
                        thread.start()
                    except Exception as e:
                        print(f"[EventBus] Error in handler: {e}")

    def get_event_history(self, limit: int = 50) -> List[Dict]:
        """Get recent event history"""
        with self._lock:
            return [event.to_dict() for event in self._event_history[-limit:]]
        
    def clear_history(self):
        """Clear event history"""
        with self._lock:
            self._event_history.clear()

event_bus = EventBus()

# File Processing Pipeline - Event-Driven Architecture

A Python application demonstrating Event-Driven Architecture (EDA) with real-time file processing and visualization.

> **Note**: This is a practical exercise to understand event-driven architecture concepts through hands-on implementation.

## Demo

![Application Demo](demo_image/Screenshot%202025-11-04%20at%2011.54.21%20PM.png)

The web interface shows real-time event streaming as files are uploaded and processed through the system.

## Features

- **Event-Driven Architecture**: Built with a custom event bus using publish-subscribe pattern
- **File Monitoring**: Automatically detects new files using Watchdog
- **Multiple Processors**: Supports CSV, JSON, Text, and Image files
- **Real-Time UI**: Web-based interface with live event streaming
- **Loose Coupling**: Processors are independent and can be added/removed easily

## Architecture

```
File Created → Event Bus → File Monitor → Processor Manager
                    ↓
            Multiple Listeners:
            - Logger
            - Web UI
            - Notification System
```

### Event Types

1. `FILE_CREATED` - New file detected
2. `FILE_PROCESSING_STARTED` - Processing begins
3. `FILE_PROCESSED` - Processing completed successfully
4. `PROCESSING_FAILED` - Processing failed
5. `NOTIFICATION_SENT` - Notification sent

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
cd file_processor
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload files through the web interface or copy them directly to:
```
file_processor/data/uploads/
```

## Project Structure

```
file_processor/
├── app.py                  # Flask application
├── event_bus.py           # Event bus implementation
├── file_monitor.py        # File monitoring with Watchdog
├── processor_manager.py   # Coordinates processors
├── processors/
│   ├── base_processor.py  # Abstract base class
│   ├── csv_processor.py   # CSV file processor
│   ├── json_processor.py  # JSON file processor
│   ├── text_processor.py  # Text file processor
│   └── image_processor.py # Image file processor
├── templates/
│   └── index.html         # Web UI
└── data/
    └── uploads/           # Upload directory (monitored)
```

## Supported File Types

- **CSV**: `.csv`
- **JSON**: `.json`
- **Text**: `.txt`, `.md`, `.log`
- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp`

## How It Works

1. **File Detection**: Watchdog monitors the uploads directory
2. **Event Publishing**: When a file is created, a `FILE_CREATED` event is published
3. **Processing**: ProcessorManager finds the appropriate processor and processes the file
4. **Event Updates**: Processing events are published to the event bus
5. **UI Updates**: Web UI receives real-time updates via Server-Sent Events

## Adding New Processors

1. Create a new processor class inheriting from `BaseProcessor`
2. Implement `can_process()`, `process()`, and `processor_name` methods
3. Register it in `ProcessorManager`

Example:

```python
from processors.base_processor import BaseProcessor

class PDFProcessor(BaseProcessor):
    def can_process(self, file_path: str) -> bool:
        return file_path.lower().endswith('.pdf')

    def process(self, file_path: str) -> dict:
        # Process PDF file
        return {"success": True, "stats": {...}}

    @property
    def processor_name(self) -> str:
        return "PDF Processor"
```

## Event-Driven Benefits Demonstrated

1. **Loose Coupling**: Processors don't know about each other
2. **Scalability**: Easy to add new processors or listeners
3. **Flexibility**: Multiple components can react to the same event
4. **Real-time Updates**: UI updates automatically via event stream
5. **Separation of Concerns**: Each component has a single responsibility

## Tech Stack

- **Python 3.x**
- **Flask** - Web framework
- **Watchdog** - File system monitoring
- **Pandas** - CSV processing
- **Pillow** - Image processing
- **Server-Sent Events** - Real-time updates

## License

MIT License

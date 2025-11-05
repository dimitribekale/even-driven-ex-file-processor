import os
import sys
import time
import json
from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from event_bus import event_bus, Event, EventType
from file_monitor import FileMonitor
from processor_manager import ProcessorManager

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "data", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

processor_manager = ProcessorManager()
file_monitor = FileMonitor(UPLOAD_FOLDER, processor_manager)

def log_event(event: Event):
    print(f"[Logger] {event.event_type.value}: {event.data}")

for event_type in EventType:
    event_bus.subscribe(event_type, log_event)

@app.route("/")
def index():
    """Serve the main page"""
    return render_template("index.html")

@app.route("/api/events", methods=["GET"])
def get_events():
    """Get the event history"""
    limit = request.args.get("limit", 50, type=int)
    events = event_bus.get_event_history(limit)
    return jsonify({"events": events})

@app.route("/api/upload", methods=["POST"])
def upload_file():
    """Upload file for processing"""
    if "file" not in request.files:
        return jsonify({"error": "No file selected"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        return jsonify({
            "success": True,
            "message": f"File {filename} uploaded successfully",
            "file_path": file_path
        })
    
@app.route('/api/events/stream')
def event_stream():
    """Server-Sent Events endpoint for real-time updates"""
    def generate():
        last_count = 0
        while True:
            events = event_bus.get_event_history(100)
            current_count = len(events)

            if current_count > last_count:
                # Send new events
                new_events = events[last_count:]
                for event in new_events:
                    yield f"data: {json.dumps(event)}\n\n"
                last_count = current_count

            time.sleep(0.5)  # Poll every 500ms

    return Response(generate(), mimetype='text/event-stream')

    
@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Get system statistiques"""
    events = event_bus.get_event_history(1000)

    stats = {
        "total_events": len(events),
        "file_created": len([e for e in events if e["event_type"] == "file_created"]),
        "files_processed": len([e for e in events if e['event_type'] == 'file_processed']),
        "processing_failed": len([e for e in events if e['event_type'] == 'processing_failed']),
        "watch_directory": UPLOAD_FOLDER
    }
    return jsonify(stats)

@app.route("/api/clear", methods=["POST"])
def clear_events():
    event_bus.clear_history()
    return jsonify({"success": True, "message": "Event history cleared"})

def start_app():
    print("="*60)
    print("File Processing Pipeline - Event-Driven Architecture")
    print("=" * 60)
    print(f"Watch Directory: {UPLOAD_FOLDER}")
    print("Web Interface: http://localhost:5000")
    print("=" * 60)

    file_monitor.start()
    app.run(debug=False, host='0.0.0.0', port=5001, threaded=True)

if __name__ == '__main__':
    start_app()
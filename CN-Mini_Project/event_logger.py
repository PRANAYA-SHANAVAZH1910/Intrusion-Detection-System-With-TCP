
import json
import time
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
LOG_FILE = LOG_DIR / "traffic_events.jsonl"


def log_event(
    source_ip,
    destination_ip,
    destination_port,
    event_type,
    status
):
    timestamp = time.time()

    event = {
        "event_type": event_type,
        "source_ip": source_ip,
        "destination_ip": destination_ip,
        "destination_port": destination_port,
        "timestamp": timestamp,
        "timestamp_utc": datetime.fromtimestamp(
            timestamp, timezone.utc
        ).isoformat(),
        "status": status
    }

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event) + "\n")

    print(json.dumps(event, indent=2))

    return event

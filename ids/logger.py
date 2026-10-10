
import json
from pathlib import Path
from datetime import datetime, timezone

LOG_DIR = Path(__file__).parent / "logs"
LOG_FILE = LOG_DIR / "ids_alerts.jsonl"


def log_alert(alert):
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    entry = alert.copy()
    entry["logged_at"] = datetime.now(timezone.utc).isoformat()

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry) + "\n")

    print(f"Alert saved to: {LOG_FILE}")

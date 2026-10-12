
import json
from collections import Counter
from pathlib import Path

LOG_FILE = Path(__file__).parent / "logs" / "traffic_events.jsonl"


def main():
    if not LOG_FILE.exists():
        print("No traffic log found. Run the traffic generator first.")
        return

    event_types = Counter()
    statuses = Counter()
    ports = Counter()
    total = 0
    invalid = 0

    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            try:
                event = json.loads(line)
                required = {
                    "event_type",
                    "source_ip",
                    "destination_ip",
                    "destination_port",
                    "timestamp",
                    "status"
                }

                if not required.issubset(event):
                    invalid += 1
                    continue

                total += 1
                event_types[event["event_type"]] += 1
                statuses[event["status"]] += 1
                ports[str(event["destination_port"])] += 1

            except (json.JSONDecodeError, TypeError):
                invalid += 1

    print("\n===== TCP TRAFFIC SUMMARY =====")
    print(f"Valid events: {total}")
    print(f"Invalid records: {invalid}")

    print("\nEvent types:")
    for name, count in sorted(event_types.items()):
        print(f"  {name}: {count}")

    print("\nConnection outcomes:")
    for name, count in sorted(statuses.items()):
        print(f"  {name}: {count}")

    print("\nEvents by destination port:")
    for port, count in sorted(ports.items(), key=lambda item: int(item[0])):
        print(f"  Port {port}: {count}")

    print("\nNote: server-accepted events and client-attempt")
    print("events are counted separately.")


if __name__ == "__main__":
    main()

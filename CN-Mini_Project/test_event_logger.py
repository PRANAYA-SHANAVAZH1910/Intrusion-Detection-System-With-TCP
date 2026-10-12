
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import event_logger


class TestEventLogger(unittest.TestCase):

    def test_log_event_writes_required_fields(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            log_file = temp_path / "traffic_events.jsonl"

            with (
                patch.object(event_logger, "LOG_DIR", temp_path),
                patch.object(event_logger, "LOG_FILE", log_file),
                patch("builtins.print")
            ):
                event = event_logger.log_event(
                    source_ip="127.0.0.1",
                    destination_ip="127.0.0.1",
                    destination_port=5000,
                    event_type="connection_attempt",
                    status="success"
                )

            self.assertEqual(event["source_ip"], "127.0.0.1")
            self.assertEqual(event["destination_ip"], "127.0.0.1")
            self.assertEqual(event["destination_port"], 5000)
            self.assertEqual(event["event_type"], "connection_attempt")
            self.assertEqual(event["status"], "success")
            self.assertIn("timestamp", event)
            self.assertIn("timestamp_utc", event)

            lines = log_file.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)

            saved_event = json.loads(lines[0])
            self.assertEqual(saved_event, event)

    def test_multiple_events_are_appended(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            log_file = temp_path / "traffic_events.jsonl"

            with (
                patch.object(event_logger, "LOG_DIR", temp_path),
                patch.object(event_logger, "LOG_FILE", log_file),
                patch("builtins.print")
            ):
                event_logger.log_event(
                    "127.0.0.1", "127.0.0.1", 5000,
                    "connection_attempt", "success"
                )
                event_logger.log_event(
                    "127.0.0.1", "127.0.0.1", 5001,
                    "connection_attempt", "connection_refused"
                )

            lines = log_file.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(
                json.loads(lines[1])["status"],
                "connection_refused"
            )


if __name__ == "__main__":
    unittest.main()

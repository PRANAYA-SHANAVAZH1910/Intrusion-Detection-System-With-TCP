
import time

from rules import check_connection_rate, check_port_scan
from traffic_monitor import TrafficMonitor
from logger import log_alert

class IntrusionDetectionSystem:
    def __init__(self):
        self.monitor = TrafficMonitor()
        self.detected_sources = set()

    def process_event(self, source_ip, destination_port, timestamp=None):
        if timestamp is None:
            timestamp = time.time()

        self.monitor.record_event(
            source_ip,
            destination_port,
            timestamp
        )

        connection_count = self.monitor.get_connection_count(source_ip)
        unique_ports = self.monitor.get_unique_ports(source_ip)

        reasons = []

        if check_connection_rate(connection_count):
            reasons.append("HIGH_CONNECTION_RATE")

        if check_port_scan(unique_ports):
            reasons.append("PORT_SCAN")

        if reasons and source_ip not in self.detected_sources:
            self.detected_sources.add(source_ip)

            alert = {
                "event": "INTRUSION_DETECTED",
                "source_ip": source_ip,
                "reason": reasons,
                "connection_count": connection_count,
                "unique_ports": unique_ports,
                "timestamp": timestamp
            }

            print("\nINTRUSION DETECTED")
            print(alert)

            log_alert(alert)

            return alert

        return None


if __name__ == "__main__":
    ids = IntrusionDetectionSystem()

    print("Testing normal traffic...")

    for _ in range(3):
        ids.process_event("10.0.0.2", 5000)

    print("Normal traffic test completed.")

    print("\nTesting suspicious traffic...")

    for port in range(5000, 5008):
        ids.process_event("10.0.0.3", port)

    print("\nIDS test completed.")

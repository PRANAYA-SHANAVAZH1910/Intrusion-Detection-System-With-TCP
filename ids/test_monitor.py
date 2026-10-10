
from traffic_monitor import TrafficMonitor

monitor = TrafficMonitor()

monitor.record_event("10.0.0.3", 5000, timestamp=100)
monitor.record_event("10.0.0.3", 5001, timestamp=101)
monitor.record_event("10.0.0.3", 5002, timestamp=102)
monitor.record_event("10.0.0.3", 5002, timestamp=103)

monitor.record_event("10.0.0.2", 5000, timestamp=103)

print("Attacker connection count:",
      monitor.get_connection_count("10.0.0.3"))

print("Attacker unique ports:",
      monitor.get_unique_ports("10.0.0.3"))

print("Normal client connection count:",
      monitor.get_connection_count("10.0.0.2"))

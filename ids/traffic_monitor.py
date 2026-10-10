
import time
from collections import defaultdict, deque

from rules import TIME_WINDOW


class TrafficMonitor:
    def __init__(self):
        self.events = defaultdict(deque)

    def record_event(self, source_ip, destination_port, timestamp=None):
        if timestamp is None:
            timestamp = time.time()

        self.events[source_ip].append((timestamp, destination_port))
        self._remove_old_events(source_ip, timestamp)

    def _remove_old_events(self, source_ip, current_time):
        cutoff = current_time - TIME_WINDOW
        source_events = self.events[source_ip]

        while source_events and source_events[0][0] < cutoff:
            source_events.popleft()

    def get_connection_count(self, source_ip):
        return len(self.events[source_ip])

    def get_unique_ports(self, source_ip):
        return len({
            port for _, port in self.events[source_ip]
        })

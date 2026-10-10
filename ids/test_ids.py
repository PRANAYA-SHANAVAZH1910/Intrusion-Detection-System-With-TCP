
from ids import IntrusionDetectionSystem

ids = IntrusionDetectionSystem()

print("\n--- TEST 1: NORMAL TRAFFIC ---")

for _ in range(3):
    ids.process_event("10.0.0.2", 5000)

print("\n--- TEST 2: PORT SCAN ---")

for port in range(6000, 6008):
    ids.process_event("10.0.0.3", port)

print("\n--- TESTS COMPLETED ---")

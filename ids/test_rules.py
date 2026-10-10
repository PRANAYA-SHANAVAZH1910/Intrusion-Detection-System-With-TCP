
from rules import check_connection_rate, check_port_scan

print("Connection rate tests:")
print("7 connections:", check_connection_rate(7))
print("15 connections:", check_connection_rate(15))

print("\nPort scan tests:")
print("3 unique ports:", check_port_scan(3))
print("8 unique ports:", check_port_scan(8))

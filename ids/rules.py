
CONNECTION_THRESHOLD = 10
PORT_THRESHOLD = 5
TIME_WINDOW = 5


def check_connection_rate(connection_count):
    return connection_count > CONNECTION_THRESHOLD


def check_port_scan(unique_ports):
    return unique_ports > PORT_THRESHOLD

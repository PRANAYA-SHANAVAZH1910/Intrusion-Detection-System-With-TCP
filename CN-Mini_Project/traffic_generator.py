
import argparse
import socket
import time

from event_logger import log_event

TARGET_IP = "127.0.0.1"
NORMAL_PORT = 5000

# Ports on your own computer only.
# Port 5000 should be listening when your server is running.
TEST_PORTS = [5000, 5001, 5002, 8000, 8080]

TIMEOUT_SECONDS = 1.0


def attempt_connection(destination_ip, destination_port, send_message=False):
    """Attempt one TCP connection and record its outcome."""

    source_ip = TARGET_IP
    status = "unknown"

    try:
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as client:
            client.settimeout(TIMEOUT_SECONDS)

            # Bind locally so the source address is known even
            # if the connection attempt fails.
            client.bind((TARGET_IP, 0))
            source_ip = client.getsockname()[0]

            try:
                client.connect((destination_ip, destination_port))
                source_ip = client.getsockname()[0]
                status = "success"

                if send_message:
                    client.sendall(
                        b"Hello from the traffic generator!"
                    )
                    response = client.recv(1024)
                    print(
                        f"Server replied: "
                        f"{response.decode('utf-8', errors='replace')}"
                    )

            except ConnectionRefusedError:
                status = "connection_refused"

            except socket.timeout:
                status = "timeout"

            except OSError as error:
                status = f"error: {error}"

    except OSError as error:
        status = f"error: {error}"

    log_event(
        source_ip=source_ip,
        destination_ip=destination_ip,
        destination_port=destination_port,
        event_type="connection_attempt",
        status=status
    )

    print(
        f"Attempt to {destination_ip}:{destination_port} "
        f"-> {status}"
    )

    return status


def generate_normal_traffic(count):
    print(f"\nGenerating {count} normal TCP connections...")

    results = []

    for number in range(count):
        print(f"\nNormal connection {number + 1}/{count}")
        results.append(
            attempt_connection(
                TARGET_IP,
                NORMAL_PORT,
                send_message=True
            )
        )
        time.sleep(0.5)

    print("\nNormal traffic summary:")
    print(f"Successful: {results.count('success')}/{count}")


def generate_port_test():
    print("\nStarting controlled localhost port test...")

    results = {}

    for port in TEST_PORTS:
        print(f"\nTesting local port {port}")
        results[port] = attempt_connection(
            TARGET_IP,
            port
        )
        time.sleep(0.3)

    print("\nPort test summary:")
    for port, status in results.items():
        print(f"127.0.0.1:{port} -> {status}")


def main():
    parser = argparse.ArgumentParser(
        description="Local TCP traffic generator"
    )
    parser.add_argument(
        "mode",
        choices=["normal", "ports"],
        help="normal: send messages to port 5000; "
             "ports: test predefined localhost ports"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="number of normal connections (default: 5)"
    )

    args = parser.parse_args()

    if args.mode == "normal":
        if not 1 <= args.count <= 100:
            parser.error("--count must be between 1 and 100")
        generate_normal_traffic(args.count)
    else:
        generate_port_test()


if __name__ == "__main__":
    main()

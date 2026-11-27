# SDN-Based Network Intrusion Detection and Response System

An SDN-based network security project that demonstrates the detection of suspicious TCP connection activity and automated traffic blocking using Software-Defined Networking (SDN).

## 1. Project Overview

Network security is an important aspect of modern communication systems. Activities such as port scanning and unusually high connection attempts can indicate potential network threats.

This project implements a Network Intrusion Detection and Response System using Software-Defined Networking. It combines an Intrusion Detection System (IDS) with a centralized SDN controller to identify suspicious traffic patterns and initiate an automated response.

When suspicious activity is detected, the IDS sends an alert to the Ryu SDN controller. The controller then installs an OpenFlow rule in the Open vSwitch (OVS) to block traffic from the identified source.

The project is implemented using Python, Mininet, Ryu, Open vSwitch, and OpenFlow.

## 2. Project Objectives

- Detect suspicious TCP connection patterns.
- Identify potential port-scanning activity.
- Monitor connection attempts using structured event logs.
- Integrate an IDS with an SDN controller.
- Automate traffic blocking using OpenFlow rules.
- Demonstrate how centralized network control can improve network security.

## 3. System Architecture

The system consists of three Mininet hosts connected to a single Open vSwitch, which is managed by a Ryu SDN controller.

### Network Components

| Component | Description | IP Address |
|---|---|---|
| H1 | Legitimate client | 10.0.0.1 |
| H2 | Victim / TCP server | 10.0.0.2 |
| H3 | Traffic generator / suspicious source | 10.0.0.3 |
| S1 | Open vSwitch | — |
| Ryu | SDN controller | — |

The TCP server runs on port `5000`.

### Architecture Diagram

The architecture diagram illustrates the interaction between the hosts, Open vSwitch, IDS, live event bridge, and Ryu controller.

![System Architecture](architecture.png)

*Replace `architecture.png` with the actual filename and relative path of the architecture image you upload to the repository.*

## 4. Working Principle

The system follows these steps:

1. **Traffic Generation:** H3 generates TCP connection attempts towards the victim server. H1 represents legitimate traffic.
2. **Event Logging:** Connection-attempt information is recorded in structured JSONL event logs.
3. **Event Monitoring:** The live event bridge monitors new events and forwards relevant information to the IDS.
4. **Intrusion Detection:** The IDS analyses connection activity and checks for suspicious patterns, including high connection rates and multiple destination ports.
5. **Alert Generation:** When a detection threshold is exceeded, the IDS generates an intrusion alert and sends an HTTP request to the Ryu controller.
6. **Automated Response:** The Ryu controller installs an OpenFlow rule in OVS to drop traffic from the identified suspicious source.

The objective is to block suspicious traffic while allowing legitimate communication to continue.

## 5. Intrusion Detection Mechanism

The IDS uses a sliding time window to analyse connection-attempt events.

The documented detection parameters are:

| Parameter | Threshold |
|---|---|
| Sliding time window | 5 seconds |
| Connection-attempt detection | More than 10 attempts |
| Port-scan detection | More than 5 unique destination ports |

When suspicious activity is identified, an `INTRUSION_DETECTED` alert is generated.

The IDS communicates with the Ryu controller through the HTTP endpoint:

`http://127.0.0.1:8080/intrusion`

## 6. Automated Response

The Ryu controller receives the intrusion alert and installs a flow rule in Open vSwitch.

The documented blocking rule uses:

- Source IP: `10.0.0.3`
- Action: Drop
- Priority: `1000`
- Hard timeout: `600 seconds`

This demonstrates how an SDN controller can dynamically modify network forwarding behaviour in response to detected threats.

## 7. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Implementation of traffic generation, logging, and IDS components |
| TCP Socket Programming | Client-server communication and connection attempts |
| Mininet | Network topology emulation |
| Ryu SDN Controller | Centralized network control and response |
| Open vSwitch (OVS) | Software-based network switching |
| OpenFlow | Communication and flow-rule management |
| JSONL | Structured traffic event logging |

## 8. Project Structure

The repository contains the following main components:

### Traffic Generation and TCP Communication

- `tcp_server.py` – Implements the TCP server.
- `tcp_client.py` – Implements TCP client communication.
- `traffic_generator.py` – Generates normal and multi-port connection attempts.
- `event_logger.py` – Records connection-attempt events in JSONL format.
- `summarize_logs.py` – Summarizes and validates traffic event logs.

### Testing

- `test_event_logger.py` – Tests event logging functionality.
- `test_traffic_generator.py` – Tests traffic generation functionality.

### IDS and SDN Integration

The IDS and controller integration components include:

- `ids.py` – Intrusion detection logic.
- `rules.py` – Detection rules and thresholds.
- `traffic_monitor.py` – Traffic event monitoring.
- `logger.py` – IDS alert logging.
- `live_event_bridge.py` – Connects traffic event logs with the IDS

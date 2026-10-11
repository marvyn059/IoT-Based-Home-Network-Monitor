# IoT-Based Home Network Monitoring System

## Overview
This project is a Python-based prototype for monitoring devices on a local home network using ARP (Address Resolution Protocol) and Scapy.

## Current Features
- Sends an ARP request to a specified local network device.
- Displays the responding device's IP address and MAC address.
- Uses Python and Scapy for network packet operations.

## Technologies Used
- Python 3
- Scapy
- Npcap
- Visual Studio Code

## Current Test
The prototype successfully received a response from the local router at `192.168.1.1`.

## How to Run
1. Install Python 3.
2. Install Npcap on Windows.
3. Install Scapy using `python -m pip install scapy`.
4. Run `python network_test.py` in the project folder.

## Scope and Limitations
This is an initial prototype that tests one local network address. A response does not indicate that a device is an IoT device or that the device is safe. Further development is required for network-wide discovery and change monitoring.

## Responsible Use
Run network tests only on networks and devices you own or have permission to monitor.
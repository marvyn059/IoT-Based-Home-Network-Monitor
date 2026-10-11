IoT-Based Home Network Monitoring System

1. Project Overview

The IoT-Based Home Network Monitoring System is a Python-based application that helps users discover devices replying on their local home network. It offers a basic web dashboard to display found IP addresses and MAC addresses and records scan outcomes in a CSV file for later analysis.

This assignment shows the pragmatic application of computer networking concepts, incorporating the Address Resolution Protocol (ARP), local network device discovery, client-server communication, and data logging.

2. Objectives

Discover devices that respond to ARP requests on an authorized local IPv4 network.

Display found device IP and MAC addresses through a web dashboard.

Record scan outcomes with timestamps in a CSV file.

Demonstrate pragmatic applications of networking protocols applying Python.

Provide an uncomplicated and elementary interface for watching and downloading scan logs.

3. Features

Web dashboard developed applying Flask.

Local network discovery employing Scapy and ARP.

Display of found IP addresses and MAC addresses.

Timestamped CSV scan logging.

Downloadable scan-history file.

Local browser-based interface.

4. Technologies Used

Python; application logic and network scanning.

Flask; web application and HTTP routes.

Scapy; creation and transmission of ARP requests.

ARP; discovery of replying devices on the local network.

HTML and CSS; dashboard structure and styling.

CSV; storage of scan outcomes.

Visual Studio Code; development environment.

Git and GitHub; source-code version control.

5. Project Structure

Iot_Network_monitor/
├── app.py
├── network_test.py
├── README.md
├── .gitignore
└── network_log.csv  (generated locally; not committed)

6. Requirements

Windows computer with Python installed.

Visual Studio Code or another Python editor.

Flask Python package.

Scapy Python package.

Npcap installed if required by the Windows Scapy configuration.

Connection to a local IPv4 network that you own or are authorized to monitor.

7. Installation and Execution

Step 1: Install dependencies

python -m pip install flask scapy

On Windows, install Npcap if it is needed for Scapy packet capture and transmission.

Step 2: Configure the network

Open app.py and check the configured network:

NETWORK = "192.168.1.0/24"

Change this value if your authorized local network uses a different IPv4 subnet.

Step 3: Run the application

---python app.py

Step 4: Open the dashboard

Visit the following address in your browser:

http://127.0.0.1:5000

Click Scan Network to discover responding devices. If the download route is present in your version of app.py, use Download CSV Log to download the saved results.

HOW IT WORKS

The user opens the Flask dashboard in a web browser.

The user clicks the network scan button.

Flask receives the scan request.

Scapy sends ARP requests to the configured local subnet.

Devices that respond are recorded with their IP and MAC addresses.

The results are displayed in the dashboard.

The application appends the results and scan timestamp to network_log.csv.

RESULT

The model has been tested on a local Windows environment. The Flask dashboard loaded successfully, scan requests was processed, and a CSV file was generated with scan timestamps, IP addresses, and MAC addresses.

Screenshots of the real running application and scan outcomes should be added to the assignment documentation after testing.

LIMITATIONS

-ARP discovery is limited to the local network segment.
- Some devices may not respond to ARP requests and may hence be absent from outcomes. 
-A found device is not necessarily an IoT device. 
-A recently found device is not automatically hostile.
- The model does not provide continuous observation, breach detection, or router-wide visibility. -Scanning may need appropriate authorizations and a correctly configured network interface.

Security and Privacy

Use this application only on networks you own or are authorized to monitor. Scan logs may contain sensitive local network information. The Flask development server is configured to listen on 127.0.0.1, so the dashboard is intended for local use rather than public deployment.

The CSV log is excluded from Git using .gitignore to help prevent accidental publication of network details.

 Future Improvements

Add a device history and comparison view.

Identify newly observed devices by comparing scans.

Add charts showing the number of devices discovered over time.

Improve interface selection and error reporting.

Add optional continuous monitoring and alerts.

Add authentication and a production-ready deployment configuration.

 

Project: IoT-Based Home Network Monitoring System
Course: Data Communication and Computer Networks (DCCN)

from flask import Flask, render_template_string, send_file
from datetime import datetime
from scapy.all import ARP, Ether, srp
import ipaddress
import csv
import os

app = Flask(__name__)

# Your local Wi-Fi subnet
NETWORK = "192.168.1.0/24"

# Save the CSV file in the same folder as app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "network_log.csv")


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Home Network Monitor</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            color: #172033;
            margin: 0;
            padding: 32px;
        }

        main {
            max-width: 950px;
            margin: auto;
        }

        header, .panel {
            background: white;
            padding: 24px;
            border-radius: 14px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px #0000000d;
        }

        .muted {
            color: #64748b;
        }

        .status {
            display: inline-block;
            background: #dcfce7;
            color: #166534;
            padding: 6px 10px;
            border-radius: 20px;
        }

        button {
            background: #2563eb;
            color: white;
            border: 0;
            border-radius: 8px;
            padding: 12px 18px;
            cursor: pointer;
            font-size: 15px;
        }

        button:hover {
            background: #1d4ed8;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            overflow-wrap: anywhere;
        }

        th, td {
            padding: 12px;
            border-bottom: 1px solid #e2e8f0;
            text-align: left;
        }

        th {
            color: #475569;
        }

        code {
            background: #f1f5f9;
            padding: 3px 6px;
            border-radius: 4px;
        }

        .error {
            color: #b91c1c;
        }

        .success {
            color: #166534;
        }

        @media (max-width: 600px) {
            body {
                padding: 12px;
            }

            header, .panel {
                padding: 16px;
            }

            th, td {
                padding: 8px 4px;
                font-size: 13px;
            }
        }
    </style>
</head>

<body>
<main>
    <header>
        <p class="muted">IOT PROJECT · NETWORK MONITORING</p>
        <h1>Home Network Monitor</h1>
        <p class="muted">
            Local network device discovery using Python and Scapy
        </p>
        <span class="status">Dashboard running</span>
    </header>

    <section class="panel">
        <h2>System Overview</h2>

        <p>
            <strong>Monitoring method:</strong>
            ARP (Address Resolution Protocol)
        </p>

        <p>
            <strong>Target network:</strong>
            <code>{{ network }}</code>
        </p>

        <p>
            <strong>Last scan:</strong>
            {{ last_scan }}
        </p>

        
<form method="POST" action="/scan"
      style="display:inline-block; margin-right:8px;">
    <button type="submit">Scan Network</button>
</form>

<a href="/download">
    <button type="button">Download CSV Log</button>
</a>


        {% if message %}
            <p class="{{ 'error' if error else 'success' }}">
                {{ message }}
            </p>
        {% endif %}
    </section>

    <section class="panel">
        <h2>Discovered Devices ({{ devices|length }})</h2>

        <p class="muted">
            These devices responded to the latest ARP scan.
            Some devices may not respond and may not appear here.
        </p>

        <table>
            <thead>
                <tr>
                    <th>No.</th>
                    <th>IP Address</th>
                    <th>MAC Address</th>
                    <th>Status</th>
                </tr>
            </thead>

            <tbody>
                {% for device in devices %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td><code>{{ device.ip }}</code></td>
                    <td><code>{{ device.mac }}</code></td>
                    <td>Responded to ARP</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="4">
                        No scan results yet. Click Scan Network.
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </section>
</main>
</body>
</html>
"""


devices = []
last_scan = "Not scanned yet"
message = ""
error = False


def save_scan_results(found_devices, scan_time):
    """Append discovered devices to the CSV log."""
    file_exists = os.path.isfile(CSV_FILE)

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(file)

        # Write column headings for a new or empty file.
        if not file_exists or os.path.getsize(CSV_FILE) == 0:
            writer.writerow([
                "Scan Time",
                "IP Address",
                "MAC Address"
            ])

        # Write one row for each device that responded.
        for device in found_devices:
            writer.writerow([
                scan_time,
                device["ip"],
                device["mac"]
            ])


@app.route("/")
def dashboard():
    return render_template_string(
        HTML,
        network=NETWORK,
        devices=devices,
        last_scan=last_scan,
        message=message,
        error=error
    )


@app.route("/download")
def download_log():
    if not os.path.isfile(CSV_FILE):
        return "No scan log exists yet. Run a scan first.", 404

    return send_file(
        CSV_FILE,
        as_attachment=True,
        download_name="network_log.csv",
        mimetype="text/csv"
    )

@app.route("/scan", methods=["POST"])
def scan_network():
    global devices, last_scan, message, error

    try:
        # Validate the configured private IPv4 network.
        network = ipaddress.ip_network(NETWORK, strict=False)

        if not network.is_private or network.version != 4:
            raise ValueError(
                "Only private IPv4 networks are allowed."
            )

        # Send ARP requests to the configured local subnet.
        packet = (
            Ether(dst="ff:ff:ff:ff:ff:ff")
            / ARP(pdst=str(network))
        )

        answered, _ = srp(
            packet,
            timeout=3,
            verbose=False
        )

        # Collect IP and MAC addresses from responses.
        devices = [
            {
                "ip": response.psrc,
                "mac": response.hwsrc
            }
            for _, response in answered
        ]

        # Sort devices by IP address.
        devices.sort(
            key=lambda item: ipaddress.ip_address(item["ip"])
        )

        last_scan = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Save this scan's results.
        save_scan_results(devices, last_scan)

        message = (
            f"Scan completed. Found {len(devices)} "
            "responding device(s). "
            "Results saved to network_log.csv."
        )
        error = False

    except Exception as exc:
        message = (
            "Scan or logging failed. Check your network, "
            "permissions, and Scapy/Npcap installation. "
            f"Details: {type(exc).__name__}: {exc}"
        )
        error = True

    return dashboard()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )

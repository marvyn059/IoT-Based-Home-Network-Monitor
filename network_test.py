
from scapy.all import ARP, Ether, srp

# Test the router on your own Wi-Fi network
target_ip = "192.168.1.1"

packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_ip)

answered, unanswered = srp(
    packet,
    timeout=3,
    verbose=False
)

if answered:
    for sent, received in answered:
        print("Device responded!")
        print("IP address:", received.psrc)
        print("MAC address:", received.hwsrc)
else:
    print("No response received. We can troubleshoot if needed.")

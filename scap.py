from scapy.all import sniff, DNSQR, DNS, IP
import sqlite3
import requests
from datetime import datetime

SERVER_URL = "http://localhost:5000/log"  # change this to your server's IP

# Local DB (optional, still logs locally)
conn = sqlite3.connect("dns_logs.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS dns_requests (
    timestamp TEXT,
    ip TEXT,
    domain TEXT
)
""")
conn.commit()


def log_to_local_db(ip, domain):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO dns_requests (timestamp, ip, domain) VALUES (?, ?, ?)",
        (timestamp, ip, domain),
    )
    conn.commit()


def send_to_server(ip, domain):
    try:
        response = requests.post(SERVER_URL, json={"ip": ip, "domain": domain})
        if response.status_code != 200:
            print(f"❌ Failed to send to server: {response.text}")
    except Exception as e:
        print(f"🔥 Server send error: {e}")


def process_packet(packet):
    if packet.haslayer(DNS) and packet.getlayer(DNS).qr == 0:
        ip = packet[IP].src
        domain = packet[DNSQR].qname.decode("utf-8").strip(".")
        log_to_local_db(ip, domain)
        send_to_server(ip, domain)
        print(f"📡 {ip} → {domain}")


print("[*] Starting DNS sniffer...")
sniff(filter="udp port 53", prn=process_packet, store=0)

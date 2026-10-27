#!/usr/bin/env python3
"""Educational network packet sniffer built with Scapy.

Use only on networks and devices you own or are explicitly authorized to monitor.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime

try:
    from scapy.all import sniff, IP, IPv6, TCP, UDP, ICMP, ARP, DNS, DNSQR, Raw
except ImportError:
    print("Error: Scapy is not installed. Run: python -m pip install -r requirements.txt", file=sys.stderr)
    raise SystemExit(1)


def packet_summary(packet) -> str:
    timestamp = datetime.now().strftime("%H:%M:%S")
    source = destination = "N/A"
    protocol = "OTHER"
    details = []

    if packet.haslayer(IP):
        source = packet[IP].src
        destination = packet[IP].dst
        protocol = "IP"
    elif packet.haslayer(IPv6):
        source = packet[IPv6].src
        destination = packet[IPv6].dst
        protocol = "IPv6"
    elif packet.haslayer(ARP):
        source = packet[ARP].psrc
        destination = packet[ARP].pdst
        protocol = "ARP"

    if packet.haslayer(TCP):
        protocol = "TCP"
        details.append(f"ports {packet[TCP].sport} -> {packet[TCP].dport}")
    elif packet.haslayer(UDP):
        protocol = "UDP"
        details.append(f"ports {packet[UDP].sport} -> {packet[UDP].dport}")
    elif packet.haslayer(ICMP):
        protocol = "ICMP"
    elif packet.haslayer(ARP):
        details.append(f"operation {packet[ARP].op}")

    if packet.haslayer(DNS) and packet.haslayer(DNSQR):
        try:
            query = packet[DNSQR].qname.decode("utf-8", errors="replace").rstrip(".")
            details.append(f"DNS query: {query}")
        except Exception:
            details.append("DNS query present")

    if packet.haslayer(Raw):
        payload_size = len(bytes(packet[Raw].load))
        details.append(f"payload {payload_size} bytes")

    length = len(packet)
    extra = " | ".join(details)
    line = f"[{timestamp}] {protocol:<5} {source} -> {destination} | {length} bytes"
    return f"{line} | {extra}" if extra else line


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture and summarize packets on an authorized network interface."
    )
    parser.add_argument("-i", "--interface", help="Interface to listen on (default: Scapy chooses one)")
    parser.add_argument("-c", "--count", type=int, default=0,
                        help="Number of packets to capture; 0 means continue until Ctrl+C (default: 0)")
    parser.add_argument("-f", "--filter", default="",
                        help='Optional BPF capture filter, e.g. "tcp" or "port 53"')
    args = parser.parse_args()

    if args.count < 0:
        parser.error("--count must be zero or a positive integer")

    print("=" * 72)
    print(" BASIC NETWORK SNIFFER — EDUCATIONAL USE")
    print("=" * 72)
    print("Capture only traffic you own or have explicit permission to monitor.")
    print(f"Interface : {args.interface or 'Scapy default'}")
    print(f"Packet cap: {args.count if args.count else 'unlimited (Ctrl+C to stop)'}")
    print(f"BPF filter: {args.filter or 'none'}")
    print("-" * 72)

    try:
        sniff(
            iface=args.interface or None,
            filter=args.filter or None,
            prn=lambda packet: print(packet_summary(packet), flush=True),
            store=False,
            count=args.count,
        )
    except PermissionError:
        print("Permission denied. On Linux, run with sudo; on Windows, use an elevated terminal and install Npcap.",
              file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"Capture error: {exc}", file=sys.stderr)
        print("Check the interface name, capture permissions, and BPF filter.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCapture stopped by user.")
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1

    print("Capture finished.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

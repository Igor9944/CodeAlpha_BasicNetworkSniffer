# CodeAlpha Basic Network Sniffer

A small, command-line **network packet sniffer written in Python with Scapy**. This project was created as an educational exercise for **CodeAlpha Cyber Security Internship — Task 1**.

It captures packets from a selected network interface and prints a readable summary with the timestamp, protocol, source and destination, packet length, ports when available, and DNS query names when visible.

> **Authorized use only:** Capture traffic only on your own devices/networks or where you have explicit permission. Follow applicable laws and your organization's policies. This tool is for learning and troubleshooting, not covert monitoring.

## Features

- Capture packets from a chosen network interface.
- Display IPv4, IPv6, ARP, TCP, UDP and ICMP traffic summaries.
- Show TCP/UDP source and destination ports.
- Display visible DNS query names.
- Limit the number of packets with `--count`.
- Apply optional Berkeley Packet Filter (BPF) expressions such as `tcp`, `udp`, or `port 53`.
- Stream output to the terminal without storing every packet in memory.
- Friendly command-line help and basic error handling.

## Requirements

- Python 3.9 or newer recommended.
- Scapy.
- Packet-capture permissions.
- On Windows, install [Npcap](https://npcap.com/) and run the terminal with appropriate privileges.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Igor9944/CodeAlpha_BasicNetworkSniffer.git
cd CodeAlpha_BasicNetworkSniffer
```

### 2. Create and activate a virtual environment (recommended)

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Usage

Some operating systems require administrator/root privileges for packet capture. Use elevated privileges only when needed and only for authorized testing.

### Basic capture

Linux:

```bash
sudo python3 sniffer.py
```

Windows (PowerShell as Administrator, after installing Npcap):

```powershell
python sniffer.py
```

### Select an interface

```bash
sudo python3 sniffer.py --interface eth0
```

Replace `eth0` with an interface available on your system. See [USER_GUIDE.md](USER_GUIDE.md) for ways to list interfaces.

### Capture a limited number of packets

```bash
sudo python3 sniffer.py --count 25
```

### Filter traffic

Capture only TCP:

```bash
sudo python3 sniffer.py --filter "tcp"
```

Capture UDP traffic:

```bash
sudo python3 sniffer.py --filter "udp"
```

Capture DNS-related traffic (port 53):

```bash
sudo python3 sniffer.py --filter "port 53"
```

Combine a filter with a packet limit:

```bash
sudo python3 sniffer.py --interface eth0 --filter "tcp" --count 50
```

### Stop capture

Press **Ctrl+C** to stop an unlimited capture.

### Show help

```bash
python3 sniffer.py --help
```

## Example output

Output varies with your network traffic and interface. An example line may look like:

```text
[14:32:08] TCP   192.168.1.10 -> 142.250.72.14 | 74 bytes | ports 51432 -> 443
[14:32:09] DNS   192.168.1.10 -> 192.168.1.1 | 75 bytes | ports 53120 -> 53 | DNS query: example.com
```

The displayed protocol may be TCP or UDP for DNS packets, depending on the packet. The sample is illustrative, not captured data.

## Project structure

```text
CodeAlpha_BasicNetworkSniffer/
├── sniffer.py       # Packet capture and terminal summaries
├── requirements.txt # Python dependency list
├── README.md        # Project overview and quick start
├── USER_GUIDE.md    # Detailed step-by-step usage guide
└── LICENSE          # MIT license
```

## Limitations

- It shows only packets visible to the selected interface; switched networks, Wi-Fi isolation, VPNs, and encryption affect what can be observed.
- It does not decrypt TLS/HTTPS traffic. Encrypted application payloads remain encrypted.
- DNS names appear only when relevant DNS packets are visible and the query is not hidden by encrypted DNS.
- BPF filter availability depends on the operating system and packet-capture backend.
- This starter project is intended for learning and does not replace a production network monitoring or intrusion detection system.

## Troubleshooting

**Permission denied:** Run the command with appropriate privileges. Avoid running unrelated commands as root.

**No packets appear:** Check that the interface is active, generate normal traffic on that interface, and confirm the interface name.

**Unknown interface:** List interfaces using the commands in [USER_GUIDE.md](USER_GUIDE.md).

**Filter error:** Start without `--filter`, then try a simple expression such as `tcp`. BPF support depends on your platform and capture backend.

**Scapy is missing:** Activate your virtual environment and run `python -m pip install -r requirements.txt`.

## Learning outcomes

- Basics of packet capture and network protocols.
- Understanding source/destination addresses and transport ports.
- Introduction to BPF capture filters.
- Responsible handling of network visibility and permissions.

## Author

**Igor9944** — [GitHub profile](https://github.com/Igor9944)

## License

Distributed under the MIT License. See [LICENSE](LICENSE).

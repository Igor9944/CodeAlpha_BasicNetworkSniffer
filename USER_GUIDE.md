# User Guide — Basic Network Sniffer

This guide walks through installing, starting, filtering, and stopping the packet sniffer.

## 1. Check Python

Linux:

```bash
python3 --version
```

Windows:

```powershell
py --version
```

Use Python 3.9 or newer if possible.

## 2. Identify your network interface

Linux:

```bash
ip -brief link
```

You may see names such as `lo`, `eth0`, `enp0s3`, or `wlan0`. Choose the active Ethernet or Wi-Fi interface, not usually `lo` (loopback).

Alternative (with Scapy installed):

```bash
python3 -c "from scapy.all import get_if_list; print('\\n'.join(get_if_list()))"
```

Windows PowerShell:

```powershell
Get-NetAdapter
```

Npcap must be installed for packet capture on Windows.

## 3. Install the project

```bash
git clone https://github.com/Igor9944/CodeAlpha_BasicNetworkSniffer.git
cd CodeAlpha_BasicNetworkSniffer
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## 4. Start capturing

Capture all visible traffic (Linux):

```bash
sudo .venv/bin/python sniffer.py
```

Capture 10 packets:

```bash
sudo .venv/bin/python sniffer.py --count 10
```

Capture TCP packets on a specific interface:

```bash
sudo .venv/bin/python sniffer.py --interface enp0s3 --filter "tcp"
```

Replace `enp0s3` with your actual interface. If using a virtual environment with sudo, use its explicit Python path as shown above.

## 5. Understand the output

- **Timestamp:** local time when the summary is printed.
- **Protocol:** observed network or transport protocol (for example TCP, UDP, ICMP, ARP, IPv6).
- **Source → Destination:** source and destination addresses, where available.
- **Bytes:** total captured packet length.
- **Ports:** TCP/UDP source and destination ports.
- **DNS query:** a domain name when a visible DNS query is present.
- **Payload size:** size of the packet's raw payload when available; payload content is not printed.

## 6. Stop the capture

If you did not set `--count`, press **Ctrl+C** in the terminal. The program should print a message and exit.

## 7. Common problems

### Permission error
Packet capture usually requires elevated permissions. On Linux, prefix the command with `sudo`. On Windows, open PowerShell as Administrator and ensure Npcap is installed.

### Empty output
Confirm the selected interface is up and that you are authorized to monitor it. Generate ordinary traffic, such as opening a website, then observe the terminal. You may not see other devices' unicast traffic on a switched network.

### Filter does not work
Try without a filter first. Then test a simple filter like `tcp` or `udp`. Filter syntax and support depend on the capture backend.

### Scapy import error
Activate the virtual environment and install dependencies again:

```bash
python -m pip install -r requirements.txt
```

## Responsible use

Only inspect traffic on systems and networks you own or have explicit permission to monitor. Do not capture other people's traffic without authorization, and do not publish packet captures containing personal or confidential information.

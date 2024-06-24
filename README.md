# Network Scanner

This Python script scans a specified IP range to find live hosts, then retrieves their MAC addresses and vendor information.

## Features

- Scans an IP range for live hosts
- Retrieves MAC addresses and vendor information for live hosts
- Displays results in a formatted table

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have a Linux system (the script uses Linux-specific commands)
- You have root access (sudo privileges)
- You have Python 3.x installed

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ApinHovo/network-scanner.git
   cd network-scanner
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. Install the necessary system tools:
   ```bash
   sudo apt-get update
   sudo apt-get install fping arp-scan
   ```

## Usage

1. Run the script with root privileges:
   ```bash
   sudo venv/bin/python main.py
   ```

2. When prompted, enter the IP range you want to scan. You can specify the range in two formats:
   - CIDR notation, e.g., "192.168.1.0/24" (scans all IPs in the 192.168.1.0 to 192.168.1.255 range)
   - Specific range, e.g., "192.168.1.100 192.168.1.200" (scans IPs from 192.168.1.100 to 192.168.1.200)

3. The script will display a table with the IP addresses, MAC addresses, and vendor information of live hosts in the specified range.

## Example Output

```
+----------------+-------------------+-------------------------------+
| IP Address     | MAC Address       | Vendor                        |
+================+===================+===============================+
| 192.168.1.1    | 00:11:22:33:44:55 | ACME Network Solutions        |
+----------------+-------------------+-------------------------------+
| 192.168.1.5    | AA:BB:CC:DD:EE:FF | TechCorp Industries           |
+----------------+-------------------+-------------------------------+
| 192.168.1.10   | 11:22:33:44:55:66 | Global Systems Inc.           |
+----------------+-------------------+-------------------------------+
```

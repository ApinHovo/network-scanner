import ipaddress
import os
import socket
import subprocess
import tempfile

import psutil
from tabulate import tabulate


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if error:
        print(f"Error: {error.decode('utf-8')}")
    return output.decode('utf-8')


def get_local_network_cidr():
    interfaces = psutil.net_if_addrs()

    for interface_name, interface_addresses in interfaces.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET and not address.address.startswith('127.'):
                network_address = address.address
                subnet_mask = address.netmask
                break
        else:
            continue
        break

    network = ipaddress.IPv4Network(f'{network_address}/{subnet_mask}', strict=False)
    cidr_range = str(network)

    return cidr_range


def get_live_hosts(ip_range):
    print("Scanning for live hosts...")
    command = f"fping -agq {ip_range}"
    output = run_command(command)
    return output.strip().split('\n')


def get_mac_and_vendor(live_hosts):
    print("Gathering MAC addresses and vendor information...")

    # Create a temporary file with live hosts
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        for host in live_hosts:
            temp_file.write(f"{host}\n")
        temp_file_name = temp_file.name

    # Run arp-scan with the temporary file
    command = f"arp-scan -g -f {temp_file_name}"
    output = run_command(command)

    # Clean up the temporary file
    os.unlink(temp_file_name)

    results = []
    for line in output.split('\n'):
        parts = line.split('\t')
        if len(parts) >= 3:
            ip = parts[0]
            mac = parts[1]
            vendor = parts[2]
            results.append([ip, mac, vendor])
    return results


def main():
    if run_command("id -u").strip() != '0':
        print("Please run as root")
        return

    default_ip_range = get_local_network_cidr()
    prompt_message = (
        f"Enter IP range (e.g., '192.168.1.0/24' or '192.168.1.100 192.168.1.200')\n"
        f"Default: '{default_ip_range}' : "
    )
    ip_range = input(prompt_message)

    # Count number of hosts to be scanned
    if not ip_range:
        ip_range = default_ip_range

    if '/' in ip_range:  # CIDR notation
        network = ipaddress.ip_network(ip_range, strict=False)
        num_hosts = network.num_addresses
    else:  # Start and end IP address range
        start_ip, end_ip = ip_range.split()
        start_ip_obj = ipaddress.ip_address(start_ip)
        end_ip_obj = ipaddress.ip_address(end_ip)
        num_hosts = int(end_ip_obj) - int(start_ip_obj) + 1

    print(f"\nNumber of hosts to be scanned: {num_hosts}\n")

    live_hosts = get_live_hosts(ip_range)
    results = get_mac_and_vendor(live_hosts)
    sorted_results = sorted(results, key=lambda x: x[0])

    headers = ["IP Address", "MAC Address", "Vendor"]
    print(tabulate(sorted_results, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()

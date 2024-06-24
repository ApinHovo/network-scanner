import os
import subprocess
import tempfile

from tabulate import tabulate


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if error:
        print(f"Error: {error.decode('utf-8')}")
    return output.decode('utf-8')


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
    command = f"arp-scan -f {temp_file_name}"
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

    ip_range = input("Enter IP range (e.g., '192.168.1.0/24' or '192.168.1.100 192.168.1.200'): ")

    live_hosts = get_live_hosts(ip_range)
    results = get_mac_and_vendor(live_hosts)

    headers = ["IP Address", "MAC Address", "Vendor"]
    print(tabulate(results, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    main()

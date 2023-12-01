import subprocess
import requests
import re
from colorama import init, Fore, Style

init()

arp_scan_output = subprocess.check_output(["sudo", "arp-scan", "--localnet"])
arp_scan_output = arp_scan_output.decode("utf-8")

pattern = r'(\d+\.\d+\.\d+\.\d+)\s+\S+\s+(.+)$'

ips_with_webpage = {}

matches = re.findall(pattern, arp_scan_output, re.MULTILINE)
for match in matches:
    ip = match[0]
    hostname = match[1]
    try:
        response = requests.get(f"http://{ip}/")
        if response.status_code == 200:
            print(Fore.GREEN + f"IP \033]8;;http://{ip}\033\\{ip}\033]8;;\033\\ ({hostname}) has a working webpage." + Style.RESET_ALL)
            ips_with_webpage[ip] = hostname
        else:
            print(Fore.RED + f"IP {ip} ({hostname}) does not have a working webpage (Status Code: {response.status_code})" + Style.RESET_ALL)
    except requests.RequestException:
        print(Fore.YELLOW + f"IP {ip} ({hostname}) is not reachable or doesn't have a webpage." + Style.RESET_ALL)

print("\n" + Fore.CYAN + "IPs with working webpages:" + Style.RESET_ALL)
for ip, hostname in ips_with_webpage.items():
    print(f"Hostname: {hostname}, IP: \033]8;;http://{ip}\033\\{ip}\033]8;;\033\\")

import ipaddress
import subprocess
from pathlib import Path

VERSION = subprocess.run(["/usr/bin/git", "rev-parse", "HEAD"], text=True, capture_output=True).stdout.strip()

class Hostnames:
    local = ["localhost", "127.0.0.1"]
    normal = ["nercone.dev", "nerc1.dev", "diamondgotcat.net", "d-g-c.net"]
    onion = "4sbb7xhdn4meuesnqvcreewk6sjnvchrsx4lpnxmnjhz2soat74finid.onion"
    all = local + normal + [onion]

class Directories:
    base = Path.cwd()
    public = base.joinpath("public")
    logs = base.joinpath("logs")
    databases = base.joinpath("databases")

class Files:
    quotes = Directories.public.joinpath("quotes.txt")
    shorturls = Directories.public.joinpath("shorturls.json")

    class Logs:
        uvicorn = Directories.logs.joinpath("uvicorn.log")
        access = Directories.logs.joinpath("access.log")

    class Databases:
        access_counter = Directories.databases.joinpath("access_counter.db")

class AccessSources:
    trusted = [
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
        "127.0.0.0/8",
        "169.254.0.0/16",

        "::1/128",
        "fc00::/7",
        "fe80::/10",

        "100.64.0.0/10"
    ]

    @staticmethod
    def is_trusted(ip: str, forwarded_for: str = "") -> bool:
        try:
            addr = ipaddress.ip_address(ip)
            networks = [ipaddress.ip_network(n) for n in AccessSources.trusted]
            ip_is_trusted = any(addr in net for net in networks)
        except ValueError:
            return False

        if not ip_is_trusted:
            return False

        if forwarded_for:
            entries = [e.strip() for e in forwarded_for.split(",")]

            proxy_idx = None
            for i in range(len(entries) - 1, -1, -1):
                try:
                    if entries[i] and ipaddress.ip_address(entries[i]) == addr:
                        proxy_idx = i
                        break
                except ValueError:
                    continue

            if proxy_idx is None:
                return True

            if proxy_idx == 0:
                return True

            effective_entry = entries[proxy_idx - 1]
            if not effective_entry:
                return True
            try:
                effective_addr = ipaddress.ip_address(effective_entry)
                return any(effective_addr in net for net in networks)
            except ValueError:
                return False

        return True

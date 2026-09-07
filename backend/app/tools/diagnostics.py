import platform
import socket
import urllib.request
from datetime import datetime


def check_internet() -> dict:
    """
    Check whether the machine can reach the internet.
    """

    test_urls = [
        "https://www.google.com",
        "https://www.cloudflare.com",
    ]

    for url in test_urls:
        try:
            request = urllib.request.Request(
                url,
                method="HEAD",
                headers={"User-Agent": "HelpDeskAI/1.0"},
            )

            with urllib.request.urlopen(request, timeout=5) as response:
                return {
                    "tool": "check_internet",
                    "status": "online",
                    "reachable": True,
                    "http_status": response.status,
                    "checked_at": datetime.now().isoformat(),
                }

        except Exception:
            continue

    return {
        "tool": "check_internet",
        "status": "offline",
        "reachable": False,
        "checked_at": datetime.now().isoformat(),
    }


def check_network() -> dict:
    """
    Check basic local network connectivity.
    """

    hostname = socket.gethostname()

    local_ip = None

    try:
        # Create a UDP socket and let the OS determine
        # the active outbound interface.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()
    except Exception:
        pass

    return {
        "tool": "check_network",
        "hostname": hostname,
        "local_ip": local_ip,
        "network_available": (
            local_ip is not None
            and not local_ip.startswith("127.")
        ),
        "checked_at": datetime.now().isoformat(),
    }


def check_system() -> dict:
    """
    Collect safe basic system information.
    """

    return {
        "tool": "check_system",
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "checked_at": datetime.now().isoformat(),
    }

import subprocess
import time

# detected interfaces
interface = None
mon_interface = None

#colors
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
purple = "\033[35m"
clear = "\033[00m"

channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

def _get_wireless_interfaces():
    """Return a list of available wireless interfaces."""
    try:
        output = subprocess.check_output("iw dev | awk '$1==\"Interface\"{print $2}'", shell=True)
        return output.decode().split()
    except subprocess.CalledProcessError:
        return []


def monitormode():
    """Enable monitor mode on the first detected wireless interface."""
    global interface, mon_interface

    print("[{y}!{c}] ENABLING {b}MONITOR{c} MODE...".format(y=yellow, b=blue, c=clear))
    interfaces = _get_wireless_interfaces()
    if not interfaces:
        exit("\n[{r}-{c}] ERROR: NO WIRELESS INTERFACE FOUND.".format(r=red, c=clear))

    interface = interfaces[0]
    try:
        subprocess.check_output("airmon-ng start {}".format(interface), shell=True)
        # find new monitor interface
        for iface in _get_wireless_interfaces():
            if iface.endswith("mon") or iface.startswith("mon"):
                mon_interface = iface
                break
        if not mon_interface:
            mon_interface = interface + "mon"

        print("[{g}+{c}] {b}MONITOR{c} MODE SUCCESSFULLY ENABLED ON {m}!".format(g=green, b=blue, c=clear, m=mon_interface))
    except subprocess.CalledProcessError:
        exit("\n[{r}-{c}] ERROR: UNABLE TO ACTIVATE {b}MONITOR{c} MODE.".format(b=blue, r=red, c=clear))

def cleanup():
    """Disable monitor mode and exit."""
    global mon_interface
    print("\n[{y}!{c}] DISABLING {b}MONITOR{c} MODE...".format(y=yellow, b=blue, c=clear))
    if mon_interface:
        try:
            subprocess.check_output("airmon-ng stop {}".format(mon_interface), shell=True)
        except subprocess.CalledProcessError:
            pass
    subprocess.check_output("airmon-ng check kill", shell=True)

    exit("[{b}LOG{p}OFF{c}]...".format(b=blue, p=purple, c=clear))

def channelhopper():
    """Cycle through wifi channels on the monitor interface."""
    global mon_interface
    channel = 1
    while channel < 12:
        try:
            subprocess.check_output("sudo iwconfig {} channel {}".format(mon_interface, channel), shell=True)
            time.sleep(0.2)

            if channel >= 11:
                channel = 1
                continue

            channel += 1
        except subprocess.CalledProcessError:
            # sometimes iwconfig responds with an error, keep going if it happens
            continue

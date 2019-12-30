DISCLAIMER: I am not responsible for any potential malicious use involved with my programs. These programs have been uploaded for educational purposes and are intended to be used in a safe, controlled environment and not with destructive intent.

# networktools
A series of Python3 programs that can be used to test networks.

# networkgrave
A tool that scans for wifi networks in the area, then sends forged deauthentication packets to each scanned network. Very effective method of jamming an entire area.

NOTE: I have written the program to pretty much only fit my need, so I've set the interface to mon0. If your monmode interface is wlan0mon or whatever, change it in the code. I will write a prompt in the program later.
# dependencies
[python3-scapy] for packet creation and sending

[airmon-ng] (aircrack-ng package) for monitor mode

# to do
Separate functions from networkgrave program into separate programs to create modules that will be used for local imports (will help with portability, future projects and readability, debugging etc.).

Fix the text coloring, layout maybe as well

Improve networkgrave functionality and capability.

Add more documentation (?)

# thats pretty much it
_WHEN THERE IS NOTHING THAT FITS YOUR NEEDS, GET YOUR OWN HANDS DIRTY_

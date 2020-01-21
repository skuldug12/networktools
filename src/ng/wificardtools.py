Learn more or give us feedback
import subprocess
import time

#colors
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
purple = "\033[35m"
clear = "\033[00m"

channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

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

def cleanup(): #after scanning and all, in order for mon mode to be deactivated and for a summary
    print("\n[{y}!{c}] DISABLING {b}MONITOR{c} MODE...".format(y=yellow,b=blue, c=clear))
    subprocess.check_output("airmon-ng check kill", shell=True)
    
    exit("[{b}LOG{p}OFF{c}]...".format(b=blue, p=purple, c=clear))

def channelhopper():
    channel = 1
    while channel < 12:
        try:
            subprocess.check_output("sudo iwconfig mon0 channel " + str(channel), shell=True)
            time.sleep(0.2)
        
            if channel >= 11:
                channel = 1
                continue
            
            channel += 1
        except: #sometimes iwconfig responds with an error, this is just to keep the chanhopper going if it happens
            continue

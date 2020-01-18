import os
#local imports
from src import wificardtools as wificard
from src import features as f
from src import menus

#colors
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
purple = "\033[35m"
clear = "\033[00m"

#if run with python3
if __name__ == "__main__":
    #sudo priviliges
    if os.geteuid() != 0:
        exit("{r}Root required!{c}".format(r=red, c=clear))
    
    menus.startscreen()
    wificard.monitormode()
    f.mainsniffer()
    try:
        f.deauth_attack()
    except KeyboardInterrupt:
        print("SHUTDOWN REQUESTED...")
        wificard.cleanup()

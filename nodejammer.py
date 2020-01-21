import os
from threading import Thread
#local imports
from src/nj import wificardtools as wificard
from src/nj import features as f

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
    
    input('''
                                              .
                 .              .   .'.     \   /
               \   /      .'. .' '.'   '  -=  o  =-
             -=  o  =-  .'   '              / | \
               / | \                          |
    _   ______  ____  ______    _____    __  _____  _____________ 
   / | / / __ \/ __ \/ ____/   / /   |  /  |/  /  |/  / ____/ __ \
  /  |/ / / / / / / / __/ __  / / /| | / /|_/ / /|_/ / __/ / /_/ /    
 / /|  / /_/ / /_/ / /___/ /_/ / ___ |/ /  / / /  / / /___/ _, _/ 
/_/ |_/\____/_____/_____/\____/_/  |_/_/  /_/_/  /_/_____/_/ |_|         
    ''')
    
    wificard.monitormode()
    
    try:
        chanhop = Thread(target=wificard.channelhopper, args=[])
        chanhop.daemon = True
        chanhop.start()
        
        while True:
            f.nodejammer()
            
    except KeyboardInterrupt:
        print("SHUTDOWN REQUESTED...")
        wificard.cleanup()

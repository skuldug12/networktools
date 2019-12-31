import subprocess

#colors
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
purple = "\033[35m"
clear = "\033[00m"

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

#startscreen
def startscreen():

    subprocess.call("clear", shell=True)

    print(menumessages[0])
    input("PRESS {b}[ENTER]{c}...\n".format(b=blue, c=clear))
    
    subprocess.call("clear", shell=True)
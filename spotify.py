from pathlib import Path
import time
import urllib.request
import json
import re

#im going to need more inmports

startup=0
invalid_chars=[":", "<", ">", "{", "}", "/", "?"]#i would put like \ and | but then i get an error and i doubt anyone will try and use those
home_dir = Path.home()
save_path = home_dir / "Music"

class color: #i found this online and thought it could help lol
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def clear():
    print("\033[H\033[2J", end="", flush=True)




while startup == 0:

    playlistUrl = input(color.BOLD+"insert the url of your playlist..."+color.END)

    if not playlistUrl or playlistUrl.strip() == "":
        print(color.RED+"invalid name..."+color.END)
        continue

    clear()

    foldername = input(color.BOLD+"name of the folder to save the songs to..."+color.END)

    if not foldername or foldername.strip() == "":
        print(color.RED+"invalid name..."+color.END)
        continue

    elif any(char in foldername for char in invalid_chars):
        print(color.RED+"cant have a file with those characters..."+color.END)
        continue

    clear()

    songsave_path = save_path / foldername
    songsave_path.mkdir(parents=True, exist_ok=True)#makes the folder if not there if it is ig it will overight it
    print(f"Folder made at: {songsave_path}")

    startup = 1

print(color.GREEN+"startup done"+color.END)

split_link = playlistUrl.split("?")[0]
print (split_link)

playliststring = split_link.split("playlist/")[1]

print (f"https://spotify.com{playliststring}")

formatedurl = f"https://open.spotify.com/embed/playlist/{playliststring}" #this is like the embded fomat so it can find the song nams

time.sleep(3)#idk why i added this i just think being able to read it for a sec would be nice lol

clear()

print(color.GREEN+"url formated"+color.END)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
#i just found these headers i hope they work

reqe = urllib.request.Request(formatedurl, headers=headers)

with urllib.request.urlopen(reqe) as response:
    rdata = response.read() #reeds the data from the page

    charset = response.headers.get_content_charset() or "utf-8"

    content = rdata.decode(charset)

    print (content)
    
pattern = r'title":"(.*?)","subtitle":"(.*?)"'

matches = re.findall(pattern, content)
print(matches)

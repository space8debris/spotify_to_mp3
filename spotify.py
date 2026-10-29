from pathlib import Path

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
    


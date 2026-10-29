from pathlib import Path

#im going to need more inmports

startup=0
invalid_chars=[":", "<", ">", "{", "}", "/", "?"]#i would put like \ and | but then i get an error and i doubt anyone will try and use those
home_dir = Path.home()
save_path = home_dir / "Music"

def clear():
    print("\033[H\033[2J", end="", flush=True)




while startup == 0:

    clear()
    playlistUrl = input("insert the url of your playlist...")

    if not playlistUrl or playlistUrl.strip() == "":
        print("invalid name...")
        continue

    clear()

    foldername = input("name of the folder to save the songs to...")

    if not foldername or foldername.strip() == "":
        print("invalid name...")
        continue

    elif any(char in foldername for char in invalid_chars):
        print("cant have a file with those characters...")
        continue

    clear()

    songsave_path = save_path / foldername
    songsave_path.mkdir(parents=True, exist_ok=True)#makes the folder if not there if it is ig it will overight it
    print(f"Folder made at: {songsave_path}")

    startup = 1

clear()
print("startup done")
    


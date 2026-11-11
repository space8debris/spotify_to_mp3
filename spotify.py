from pathlib import Path
import time
import urllib.request
import json
import re
import yt_dlp
import urllib.parse
from yt_dlp.utils import match_filter_func, MaxDownloadsReached
from concurrent.futures import ThreadPoolExecutor,as_completed
import unicodedata

#pip install -U "yt-dlp[default]"

#winget install DenoLand.Deno


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


def clean(name):
    name = name.replace("\xa0", " ")
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name.strip(' .')



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
    
m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', content, re.S)
data = json.loads(m.group(1))
tracks = data["props"]["pageProps"]["state"]["data"]["entity"]["trackList"]

matches = [
    (t["title"], t["subtitle"].replace("\xa0", " "), t["duration"])
    for t in tracks
]

time.sleep(2)
clear()

print(color.GREEN+"song names and artest found"+color.END)

#####THESE are based on sunnify there not coppeyd but there based on it
def norm(text):
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    text = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", text)
    text = re.sub(r"\b(feat\.?|ft\.?)\s+.*$", "", text)
    text = text.replace("'", "").replace("’", "")
    text = "".join(c if (c.isspace() or unicodedata.category(c)[0] in "LNM") else " " for c in text)
    return re.sub(r"\s+", " ", text).strip()


def title_ok(yt_title, spotify_title):
    target = norm(spotify_title.split(" - ")[0])
    yt = norm(yt_title)
    if not target or not yt:
        return False
    if len(target) >= 4:
        return target in yt
    return target in yt.split()


def artist_ok(entry, artist):
    names = [norm(a).replace(" ", "") for a in artist.split(",")]
    if not any(re.search(r"[a-z0-9]", n) for n in names):
        return True  # artist only in non-latin script, YouTube usually romanizes it
    haystack = norm(entry.get("title")) + " " + norm(entry.get("channel") or entry.get("uploader"))
    haystack = haystack.replace(" ", "")
    return any(n and n in haystack for n in names)


def search_candidates(query):
    opts = {'quiet': True, 'no_warnings': True, 'extract_flat': True,
            'skip_download': True, 'ignoreerrors': True,
            'retries': 5, 'socket_timeout': 15}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"ytsearch5:{query}", download=False)
    return [e for e in ((info or {}).get("entries") or []) if e]


def pick_best(entries, title, artist, target_sec):
    pool = [e for e in entries
            if e.get("duration")
            and title_ok(e.get("title"), title)
            and artist_ok(e, artist)]
    if not pool:
        return None
    best = min(pool, key=lambda e: abs(e["duration"] - target_sec))
    if abs(best["duration"] - target_sec) > 30:
        return None
    return best.get("url") or f"https://www.youtube.com/watch?v={best['id']}"

def song(title, artist, duration_ms):
    target = int(duration_ms) / 1000
    filename = clean(title)
    mp3_path = songsave_path / (filename + ".mp3")

    if mp3_path.exists():
        return f"you already have: {title}"

    print(f"Downloading: {artist} - {title}")

    first_artist = artist.split(",")[0].strip()
    simple_title = re.sub(r"[(\[{].*?[)\]}]", " ", title)
    simple_title = re.sub(r"\s+", " ", simple_title).strip()
    queries = list(dict.fromkeys([
        f"{first_artist} {title}",
        f"{first_artist} {simple_title}",
        f"{simple_title} {first_artist} audio",
    ]))

    url = None
    for q in queries:
        try:
            entries = search_candidates(q)
        except Exception:
            continue
        url = pick_best(entries, title, artist, target)
        if url:
            break

    if not url:
        return f"no match :( {title}"

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'noprogress': True,
        'outtmpl': str(songsave_path / filename.replace('%', '%%')) + '.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
        ],
        'postprocessor_args': {
            'extractaudio': ['-metadata', f'artist={artist}', '-metadata', f'title={title}'],
        },
    }

    last_error = ""
    for attempt in range(3):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            break
        except Exception as e:
            last_error = str(e)
            time.sleep(2 * (attempt + 1))

    if mp3_path.exists():
        return f"done: {title}"
    return f"download failed: {title} ({last_error})"

seen = set()
unque = []
for track in matches:
    key = clean(track[0]).lower()
    if key in seen:
        continue
    seen.add(key)
    unque.append(track)

with ThreadPoolExecutor(max_workers=4) as pool:
    futures = []
    for track in unque:
        futures.append(pool.submit(song, *track))

    for future in as_completed(futures):
        print(future.result())

# spotify_to_mp3

spotify to mp3 does about what the name says; it is a lightweight script that takes a public Spotify playlist URL and downloads each song on the playlist with some metadata (no cover art yet)



How it works:<br>
It takes the URL you input and then turns it into an embedded URL so the web agent can go to the page with no need for a Spotify dev account
and pull the HTML data and sift through it to find the song title and artist of the song. It also finds the duration of the song to help 
prevent getting a slowed or sped-up version of the song. It then takes the title and all the info and, using yt-dlp, finds a video of the
song and downloads it as an mp3.



Known problems:<br>
has a 100~ song cap (I have an idea on how to fix) <br>
skips some songs (I kind of know how to fix this) <br>
takes a long time (I am working on adding parallel downloads to fix this) <br>
does not add the cover art to the metadata of the song <br>




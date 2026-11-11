# spotify_to_mp3

spotify to mp3 does about what the name says; it is a lightweight script that takes a public Spotify playlist URL and downloads each song on the playlist with some metadata (no cover art yet)



How it works:<br>
It takes the URL you input and then turns it into an embedded URL so the web agent can go to the page with no need for a Spotify dev account
and pull the HTML data and sift through it to find the song title and artist of the song. It also finds the duration of the song to help 
prevent getting a slowed or sped-up version of the song. It then takes the title and all the info and, using yt-dlp, finds a video of the
song and downloads it as an mp3.



Known problems:<br>
1.has a 100~ song cap (I have an idea on how to fix) <br>
2.does not add the cover art to the metadata of the song <br>
3.Add a ui 
4.if a vid is age restricted after a while it needs cookies to fix i found a guide on how to fix i just need to



# Script to extract lyrics from lyrics.com of various artists and save them locally

import os
import requests
from bs4 import BeautifulSoup as bs
import random
import string

pathToArtistNames = "./artists.txt"
pathToLyrics = './lyrics/'
lyricsSite = 'https://www.lyrics.com/'
artistSitePrefix = lyricsSite + 'artist/'
songLimit = 15

# the expected lyrics.com artist page does not lead to best page for quite a few artists
urlExceptions = {'Shawn Mendes': '2979091', 'Bastille': '2528804', 'Sam Smith': '2213398', 'The Chainsmokers': '2737962',
                 'James Arthur': '2743882', 'Charlie Puth': '3047262', 'Hailee Steinfeld': '2978221', 'Doja Cat': '3044004',
                 'Alessia Cara': '3098542', 'Niall Horan': '2557379', 'Tori Kelly': '2420321', 'Anne-Marie': '3024696',
                 'Post Malone': '3128337', 'Twenty One Pilots': '2101949', 'Daya': '1172429', 'Lukas Graham': '2768289'}

# to prevent repeated songs, skip collecting lyrics for songs with these words in title
skipPhrases = {"made popular by", "extended version", "music video", "album version", "acoustic", "live version", "dvd",
             "radio mix", "radio edit", "remix", "club mix", "vocal mix", "dance mix", "karaoke", "acapella"}

if not os.path.exists(pathToLyrics):
    os.makedirs(pathToLyrics)

# loop through all artists
fh = open(pathToArtistNames, "r")
for artist in fh:
    artist = artist[:-1].title()
    print("Collecting songs for: {}".format(artist))

    url = artistSitePrefix + artist.replace(' ', '-')  # format for lyrics.com artist page
    # add specific extension to url for exception artists
    if artist in urlExceptions:
        url += '/' + urlExceptions[artist]
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    
    # skip if url does not lead to lyrics.com artist page
    if not soup.find('p', {'class': 'artist-bio'}):
        print("{} is not an artist page url".format(url))
        continue

    # make subfolder for artist
    pathToArtist = pathToLyrics + artist + "/"
    if not os.path.exists(pathToArtist):
        os.makedirs(pathToArtist)

    # extract artist songs and shuffle order
    songs = soup.find_all('td', {'class': 'tal qx'})
    random.shuffle(songs)

    # loop through artist's songs
    songsAdded = set()
    for song in songs:
        # limit number of songs collected for each artist
        if len(songsAdded) == songLimit:
            break

        songTitle = song.get_text().translate({ord(char):'' for char in string.punctuation}).lower().rstrip()
        # skip repeat songs and any kind of remix
        if songTitle in songsAdded or any(skip in songTitle for skip in skipPhrases):
            continue
        
        songUrl = lyricsSite + song.find('a', href=True)["href"]  # format for lyrics.com song page
        songResponse = requests.get(songUrl)
        songSoup = bs(songResponse.text, "html.parser")
      
        # skip if url does not lead to lyrics.com lyrics page
        lyrics = songSoup.find(id="lyric-body-text")
        if not lyrics:
            print("{} is not a song page url".format(songUrl))
            continue
        
        # save to file locally
        pathToSong = pathToArtist + songTitle + ".txt"
        fh2 = open(pathToSong, 'w')
        fh2.write(songTitle + "\n")  # save song title as first line
        fh2.write(lyrics.get_text())
        fh2.close()
        songsAdded.add(songTitle)
fh.close()
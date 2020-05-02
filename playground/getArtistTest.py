### Test script to extract lyrics of songs by an artist from lyrics.com ###

from bs4 import BeautifulSoup as bs
import requests
import random

artist = "camila cabello"
songLimit = 5

url = "https://www.lyrics.com/artist/" + artist.title().replace(' ', '-')
response = requests.get(url)
soup = bs(response.text, "html.parser")

songs = soup.find_all('td', {'class': 'tal qx'})
# shuffle list of songs found
random.shuffle(songs)
# limit number of songs collected to songsToGet
songs = songs if len(songs) <= songLimit else songs[:songLimit]

for song in songs:
    print("\n~~~ {} ~~~".format(song.get_text()))
    url = "https://www.lyrics.com" + song.find('a', href=True)["href"]
    song_response = requests.get(url)
    song_soup = bs(song_response.text, "html.parser")
    lyrics = song_soup.find(id="lyric-body-text").get_text()
    print(lyrics)
### Test script to generate and access the artist page url on lyrics.com for all our artists ###

from bs4 import BeautifulSoup as bs
import requests


def isArtistPage(url):
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    
    if not soup.find('p', {'class': 'artist-bio'}):
        print("{} is not an artist page url".format(url))


f = open("artists.txt", "r")
for artist in f:
    artist = artist[:-1]  # drop newline at end
    print(artist)
    url = "https://www.lyrics.com/artist/" + artist.title().replace(' ', '-')
    isArtistPage(url)
f.close()
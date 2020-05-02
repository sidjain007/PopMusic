### Test script to extract lyrics of a song (url provided) from lyrics.com ###

from bs4 import BeautifulSoup as bs
import requests
from collections import Counter
from nltk.util import ngrams

url = "https://www.lyrics.com/lyric/34728070/Camila+Cabello/Never+Be+the+Same"
response = requests.get(url)
soup = bs(response.text, "html.parser")

lyrics = soup.find(id="lyric-body-text").get_text()
print(lyrics)

# save the lyrics to a file locally
f = open("camila+cabello=never+be+the+same.txt", "w")
f.write(lyrics)
f.close()

# drop punctuation, convert to lowercase, and split into words
punctToDrop = '().,!?"'
words = lyrics.translate({ord(char):'' for char in punctToDrop}).lower().split()

# get the n=1 to n=4 gram frequencies
unigrams = Counter(words)
bigrams = Counter(ngrams(words, 2))
trigrams = Counter(ngrams(words, 3))
fourgrams = Counter(ngrams(words, 4))

print("\nTrigram counts for this song:\n")
print(trigrams)
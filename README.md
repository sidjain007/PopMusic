# PopMusic

(Summary TODO)

1. `$ python3 extract.py`

* Script will webscrap _lyrics.com_ and save songs by 150 artists locally in folder _lyrics_  
* Modify _artists.txt_ to choose artists to get lyrics for 
* Change _songLimit_ to limit number of songs saved per artist

2. `Run stats.ipynb`

* See stats about the collected data, such as average words per song  
and the most frequent words and phrases in song titles and lyrics.  
* Interactively see lyric breakdown of a particular artist and popularity of a particular word  
* Compare the similarity of words used by artists on 3 metrics:  
        --> Jaccard Similarity (|intersection| / |union|)  
        --> Cosine Similarity on normalized word counts (TF)  
        --> Cosine Similarity on normalized word counts with IDF weighting (TFIDF)  

3. `Run generate.ipynb`

* Learn the data to auto-generate new pop song lyrics  

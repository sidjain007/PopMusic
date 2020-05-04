# PopMusic

Analyzing the lyrics of modern pop music and attempting to auto-generate new lyrics  

1. `$ python3 extract.py`

* Webscrap _lyrics.com_ to collect lyrics on 2000+ songs by 150 trending artists  
(Expect this to take a couple of hours)  

2. `Run stats.ipynb`

* See stats like the average words per song and the most frequent words and phrases in song titles and lyrics  
* Interactively see lyric breakdown of a particular artist and popularity of a particular word  
* Compare the similarity of words used by artists on 3 metrics:  
        --> Jaccard Similarity (|intersection| / |union|)  
        --> Cosine Similarity on normalized word counts (TF)  
        --> Cosine Similarity on normalized word counts with IDF weighting (TFIDF)  

3. `Run generate.ipynb`

* Auto-generate new lyrics using a bigram Markov model  

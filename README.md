# PopMusic

Analyzing the lyrics of modern pop music and attempting to auto-generate new lyrics  

1. `$ python3 extract.py`

* Webscrap _lyrics.com_ to collect lyrics on 2800 songs by 150 trending artists  
(Takes ~1 hour)  
* Skip with `loadFromPickle = True` in stats.ipynb and generate.ipynb

2. `Run stats.ipynb`

* See stats like the average words per song and the most frequent words and phrases in song titles and lyrics  
* Interactively see lyric breakdown of a particular artist and popularity of a particular word  
* Compare the similarity of words used by artists on 3 metrics:  
        --> Jaccard Similarity (|intersection| / |union|)  
        --> Cosine Similarity on normalized word counts (TF)  
        --> Cosine Similarity on normalized word counts with IDF weighting (TFIDF)  

3. `Run generate.ipynb`

* Auto-generate new lyrics using a bigram Markov model  

Some of my favorite generations:  

> im pretty sure that hes a slob  
hes such a   
permanent monday  

-----  

> every one can hold me better than that  
did you think i need you here  
 
-----  

> forget your troubles  
come back be here stargazing   
ill be better  
and we both know 

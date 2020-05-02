import string
from random import random
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from prettytable import PrettyTable

stopWords = set(stopwords.words('english'))


def tokenizeSentence(sentence, regex):
    """
    Splits sentence into list of words after dropping punctuation and lowercasing
    """

    sentence = sentence.translate({ord(char):'' for char in string.punctuation}).lower()
    return regex.findall(sentence)


def plotBarGraph(data, n, title, artist):
    """
    Plots bar graph of most frequent n-grams
    """
    
    # Plot title formatting
    if title:
        titleEnd = "Modern Pop Song Titles"
    elif artist:
        titleEnd = artist + " Songs"
    else:
        titleEnd = "Modern Pop Songs"
    
    labels = []
    counts = []
    for x in data:
        label = x[0] if n == 1 else ' '.join(x[0])
        labels.append(label)
        counts.append(x[1])
    
    rgb = (random(), random(), random())
    plt.figure(figsize=(10,5))
    plt.bar(labels, counts, align='center', width=0.75, color=rgb)
    plt.xticks(rotation=90)
    plt.rc('xtick', labelsize=13) 
    plt.xlabel('{}-gram'.format(n))
    plt.ylabel('Count')
    plt.title('Top {} Most Common {}-grams in {}'.format(len(data), n, titleEnd))
    plt.show()


def plotPieChart(word, used):
    """
    Plots pie chart of % of artists who used a word
    """

    labels = ["used", "didn't use"]
    sizes = [used, 100 - used]
    if used == 100:
        sizes = [used]
        labels = ["used"]
        
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title("% of Artists who used `{}`\n".format(word))
    plt.show()


def displayArtistWords(artist, artists, allWords, counts):
    """
    Plots bar graph of words most used by an artist
    """

    artist = artist.title()
    if artist not in artists:
        print("No lyrics were collected on {}".format(artist))
        return

    idx = artists[artist]
    words = sorted([x for x in zip(allWords, counts[idx]) if x[0] not in stopWords], reverse=True, key=lambda tup: tup[1])[:30]
    plotBarGraph(words, 1, False, artist)


def getWordStats(word, wordIdxs, counts, allArtists):
    """
    Prints stats about a word's occurences in lyric data
    """

    # find index for desired word
    if word not in wordIdxs:
        print("No artist used {}".format(word))
        return

    idx = wordIdxs[word]
    usedWord = []
    # loop through artists to see which have used word
    for i in range(len(allArtists)):
        cur = counts[i][idx]
        if cur > 0:
            usedWord.append((cur, allArtists[i]))
    
    used = len(usedWord) / len(allArtists) * 100
    plotPieChart(word, used)
    
    print("\nAnd these artists used {} the most\n".format(word))
    table = PrettyTable(['Artist', 'Uses of ' + word])
    for x in sorted(usedWord, reverse=True)[:5]:
        table.add_row([x[1], x[0]])
    print(table)


def jaccardSimilarity(set1, set2):
    """
    Returns the Jaccard Similarity between two sets
    """

    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)


def compareTwoArtists(idx1, idx2, tf, tfidf, allWords):
    """
    Returns various metrics comparing the words of two artists
    """

    words1 = set()
    words2 = set()
    for i in range(len(allWords)):
        if tf[idx1][i] > 0:
            words1.add(allWords[i])
        if tf[idx2][i] > 0:
            words2.add(allWords[i])

    js = round(jaccardSimilarity(words1, words2), 3)
    cos1 = round(cosine_similarity(tf[idx1].reshape(1, -1), tf[idx2].reshape(1, -1))[0][0], 3)
    cos2 = round(cosine_similarity(tfidf[idx1].reshape(1, -1), tfidf[idx2].reshape(1, -1))[0][0], 3)
    return js, cos1, cos2


def compareArtists(artist1, artist2, artists, tf, tfidf, allWords):
    """
    Compares 2 artists or finds the most similar artists to artist1 if artist2 is None
    """

    comparison = False
    artist1 = artist1.title()
    if artist1 not in artists:
            print("No lyrics collected on {}".format(artist1))
            return
    if artist2:
        artist2 = artist2.title()
        if artist2 not in artists:
            print("No lyrics collected on {}".format(artist2))
            return
        comparison = True

    idx1 = artists[artist1]
    if comparison:
        print("\tComparing {} and {}\n".format(artist1, artist2))
        table = PrettyTable(['Jaccard Similarity', 'TF Cosine Similarity', 'TFIDF Cosine Similarity'])
        table.add_row(compareTwoArtists(idx1, artists[artist2], tf, tfidf, allWords))
        print(table)  
    else:
        print("\nArtists with most similar vocabulary to {}\n".format(artist1))
        scores = []
        for artist2 in artists:
            if artist2 == artist1:
                continue
            idx2 = artists[artist2]
            scores.append((cosine_similarity(tfidf[idx1].reshape(1, -1), tfidf[idx2].reshape(1, -1))[0][0], artist2))

        table = PrettyTable(['Artist', 'Jaccard Similarity', 'TF Cosine Similarity', 'TFIDF Cosine Similarity'])
        for _, artist2 in sorted(scores, reverse=True)[:5]:
            js, cos1, cos2 = compareTwoArtists(idx1, artists[artist2], tf, tfidf, allWords)
            table.add_row([artist2, js, cos1, cos2])
        print(table)
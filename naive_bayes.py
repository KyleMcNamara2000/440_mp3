# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018
import math
import nltk
nltk.download('stopwords')
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

"""
This is the main entry point for MP3. You should only modify code
within this file and the last two arguments of line 34 in mp3.py
and if you want-- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


def helperBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter --laplace (1.0 by default)
    pos_prior - The prior probability that a word is positive. You do not need to change this value.
    """
    # TODO: Write your code here
    # return predicted labels of development set

    #P(positive given words) = P(positive) * product(word | type= positive)
    #initial runthrough

    positiveWords = 0
    negativeWords = 0
    positiveCounts = {}
    negativeCounts = {}
    uniqueWords = [0, 0]
    for i in range(len(train_labels)):
        if train_labels[i] == 1:
            #positiveCount += 1
            positiveWords += len(train_set[i])
            for word in train_set[i]:
                newWord = word.lower()
                if newWord in positiveCounts:
                    positiveCounts[newWord] += 1
                else:
                    positiveCounts[newWord] = 1
                    uniqueWords[0] += 1
        else:
            #negativeCount += 1
            negativeWords += len(train_set[i])
            for word in train_set[i]:
                newWord = word.lower()
                if newWord in negativeCounts:
                    negativeCounts[newWord] += 1
                else:
                    negativeCounts[newWord] = 1
                    uniqueWords[1] += 1
    totalWords = positiveWords + negativeWords


    #now do dev data
    pairs = [] #(probPos, probNeg)
    vPos = uniqueWords[0]
    vNeg = uniqueWords[1]
    for data in dev_set:
        probPositive = math.log(pos_prior)    #probPositive = math.log(float(positiveWords) / totalWords)  # P(positive)
        probNegative = math.log(1 - pos_prior)  # P(negative)
        #probPositive = math.log(float(positiveWords) / totalWords)  # P(positive)
        #probNegative = math.log(float(negativeWords) / totalWords)  # P(negative)
        for word in data:
            newWord = word.lower()
            if newWord in positiveCounts:
                probPositive += math.log((float(positiveCounts[newWord])+smoothing_parameter)/(positiveWords + smoothing_parameter * (vPos + 1)))
            else:
                probPositive += math.log(
                    (0.0 + smoothing_parameter) / (positiveWords + smoothing_parameter * (vPos + 1)))
            if newWord in negativeCounts:
                probNegative += math.log((float(negativeCounts[newWord])+smoothing_parameter)/(negativeWords + smoothing_parameter * (vNeg + 1)))
            else:
                probNegative += math.log(
                    (0.0 + smoothing_parameter) / (negativeWords + smoothing_parameter * (vNeg + 1)))
        pairs.append((probPositive, probNegative))

    return pairs


def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter=1, pos_prior=0.8):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter --laplace (1.0 by default)
    pos_prior - The prior probability that a word is positive. You do not need to change this value.
    """
    # TODO: Write your code here
    # return predicted labels of development set
    pairs = helperBayes(train_set, train_labels, dev_set, smoothing_parameter, pos_prior)
    guesses = []
    for pair in pairs:
        guesses.append(int(pair[0] > pair[1]))
    return guesses


def makePairs(train_set, stop = False):
    ps = PorterStemmer() #ps.stem(w))
    retSet = []
    badWords = stopwords.words('english')
    for i in range(len(train_set)):
        pairs = []
        for j in range(len(train_set[i]) - 1):
            if stop is False or (train_set[i][j] not in badWords and train_set[i][j + 1] not in badWords):
                #pairs.append(ps.stem(train_set[i][j]) + " " + ps.stem(train_set[i][j + 1]))
                pairs.append(train_set[i][j] + " " + train_set[i][j + 1])
        retSet.append(pairs)
    return retSet


def bigramBayes(train_set, train_labels, dev_set, unigram_smoothing_parameter=1.0, bigram_smoothing_parameter=1.0, bigram_lambda=0.01,pos_prior=0.8):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    unigram_smoothing_parameter - The smoothing parameter for unigram model (same as above) --laplace (1.0 by default)
    bigram_smoothing_parameter - The smoothing parameter for bigram model (1.0 by default)
    bigram_lambda - Determines what fraction of your prediction is from the bigram model and what fraction is from the unigram model. Default is 0.5
    pos_prior - The prior probability that a word is positive. You do not need to change this value.
    """
    # TODO: Write your code here
    # return predicted labels of development set using a bigram model
    #first make list of word pairs
    train_set_pairs = makePairs(train_set, True)
    dev_set_pairs = makePairs(dev_set, True)
    biOut = helperBayes(train_set_pairs, train_labels, dev_set_pairs, bigram_smoothing_parameter, pos_prior)
    uniOut = helperBayes(train_set, train_labels, dev_set, unigram_smoothing_parameter, pos_prior)
    guesses = []
    #for each doc: mixed = (1-L)(uniOut[i]) + (L)(biOut[i]) <- do for positive and negative
    for i in range(len(biOut)):
        mixedPositive = (1 - bigram_lambda) * uniOut[i][0] + bigram_lambda * biOut[i][0]
        mixedNegative = (1 - bigram_lambda) * uniOut[i][1] + bigram_lambda * biOut[i][1]
        guesses.append(int(mixedPositive > mixedNegative))

    return guesses
import nltk
import numpy as np


def tokenize(sentence):
    return nltk.word_tokenize(sentence, language='spanish')


def bagOfWords(tokenizedSentence, allWords):
    bag = np.zeros(len(allWords), dtype=np.float32)
    for index, w in enumerate(allWords):
        if w in tokenizedSentence:
            bag[index] = 1.0

    return bag

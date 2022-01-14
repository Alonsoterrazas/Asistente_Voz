import nltk


def tokenize(sentence):
    return nltk.word_tokenize(sentence, language='spanish')


def bagOfWords(tokenizedSentence, allWords):
    pass

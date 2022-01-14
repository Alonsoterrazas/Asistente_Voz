import json
from nltkUtils import tokenize

with open('intents.json', 'r') as f:
    intents = json.load(f)

allWords = []
tags = []
xy = []
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        allWords.extend(w)
        xy.append((w, tag))

ignoreWords = ['?', '!', ',', '.']
allWords = [w for w in allWords if w not in ignoreWords]
allWords = sorted(set(allWords))
print(allWords)

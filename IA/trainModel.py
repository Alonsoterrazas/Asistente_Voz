import os
import torch
import torch.nn as nn
from assistantDataSet import AssistantDataSet
from model import NeuralNet
from nltkUtils import tokenize, bagOfWords
import numpy as np
from torch.utils.data import DataLoader
import mysql.connector
from mysql.connector import OperationalError
from decouple import config


def getIntents():
    connection = mysql.connector.connect(
        host=config('DB_HOST'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        database=config('DB_DATABASE')
    )

    try:
        cursor = connection.cursor()
    except OperationalError:
        connection.reconnect()
        cursor = connection.cursor()

    cursor.execute('SELECT tag, pattern FROM trainData')
    intentsDB = cursor.fetchall()

    return intentsDB


intents = getIntents()

allWords = []
tags = []
xy = []
for intent in intents:
    try:
        tags.index(intent[0])
    except ValueError:
        tags.append(intent[0])

    w = tokenize(intent[1])
    allWords.extend(w)
    xy.append((w, intent[0]))

ignoreWords = ['?', '!', ',', '.']
allWords = [w for w in allWords if w not in ignoreWords]
allWords = sorted(set(allWords))

XTrain = []
YTrain = []
for (pattern, tag) in xy:
    bag = bagOfWords(pattern, allWords)
    XTrain.append(bag)

    label = tags.index(tag)
    YTrain.append(label)

XTrain = np.array(XTrain)
YTrain = np.array(YTrain)

# Hyperparams
batch_size = 8
hiddenSize = 8
outputSize = len(tags)
inputSize = len(XTrain[0])
learning_rate = 0.001
numEpochs = 250

dataset = AssistantDataSet(XTrain, YTrain)
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(inputSize, hiddenSize, outputSize).to(device)

# Train - Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(numEpochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)

        # forward
        outputs = model(words)
        loss = criterion(outputs, labels)

        # backward and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f'epoch {epoch + 1}/{numEpochs}, loss={loss.item():.4f}')

print(f'final loss, loss={loss.item():.4f}')

data = {
    'model_state': model.state_dict(),
    'input_size': inputSize,
    'output_size': outputSize,
    'hidden_size': hiddenSize,
    'all_words': allWords,
    'tags': tags
}

PATH = 'C:\\ProgramData\\Asistente\\Data'
FILE = 'data.pth'
try:
    torch.save(data, f'{PATH}\\{FILE}')
except FileNotFoundError:
    os.mkdir(PATH)
    torch.save(data, f'{PATH}\\{FILE}')

print(f'training complete. file saved to {FILE}')


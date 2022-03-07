import torch
from IA.model import NeuralNet
from IA.nltkUtils import bagOfWords, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

PATH = 'C:\\ProgramData\\Asistente\\Data\\data.pth'
data = torch.load(PATH)

input_size = data['input_size']
hidden_size = data['hidden_size']
output_size = data['output_size']
all_words = data['all_words']
tags = data['tags']
model_state = data['model_state']

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


def predictCommand(sentence):
    sentence = tokenize(sentence)
    X = bagOfWords(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    probs = probs[0]
    cont = 0
    for p in probs:
        print(f'{tags[cont]} -> prob = {p}')
        cont += 1
    prob = probs[predicted.item()]
    if prob.item() > 0.65:
        return tag

    return None

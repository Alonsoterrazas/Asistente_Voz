from os.path import exists

import torch
from IA.model import NeuralNet
from IA.nltkUtils import bagOfWords, tokenize


class IaModel:

    def __init__(self):
        self.active = False

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        PATH = 'C:\\ProgramData\\Asistente\\Data\\data.pth'
        if exists(PATH):
            self.active = True
            self.data = torch.load(PATH)

            self.input_size = self.data['input_size']
            self.hidden_size = self.data['hidden_size']
            self.output_size = self.data['output_size']
            self.all_words = self.data['all_words']
            self.tags = self.data['tags']
            self.model_state = self.data['model_state']

            self.model = NeuralNet(self.input_size, self.hidden_size, self.output_size).to(device)
            self.model.load_state_dict(self.model_state)
            self.model.eval()

    def predictCommand(self, sentence):
        if self.active:
            sentence = tokenize(sentence)
            X = bagOfWords(sentence, self.all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X)

            output = self.model(X)
            _, predicted = torch.max(output, dim=1)
            tag = self.tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            probs = probs[0]
            cont = 0
            for p in probs:
                print(f'{self.tags[cont]} -> prob = {p}')
                cont += 1
            prob = probs[predicted.item()]
            if prob.item() > 0.65:
                return tag

        return None

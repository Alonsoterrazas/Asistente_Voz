from torch.utils.data import Dataset


class AssistantDataSet(Dataset):
    def __init__(self, XTrain, YTrain):
        self.nSamples = len(XTrain)
        self.XData = XTrain
        self.YData = YTrain

    def __getitem__(self, index):
        return self.XData[index], self.YData[index]

    def __len__(self):
        return self.nSamples

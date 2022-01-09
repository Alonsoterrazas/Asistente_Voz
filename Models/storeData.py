import pickle
import os

directoryPath = 'C:\\ProgramData\\Asistente'


def saveObjectOnPickle(obj, fileName):
    try:
        pickle.dump(obj, open(f'{directoryPath}\\{fileName}.pkl', 'wb'))
        return True
    except pickle.PickleError:
        return False
    except FileNotFoundError:
        os.mkdir(directoryPath)
        saveObjectOnPickle(obj, fileName)


def getObjectFromPickle(fileName):
    try:
        obj = pickle.load(open(f'{directoryPath}\\{fileName}.pkl', 'rb'))
        return obj
    except pickle.PickleError:
        return False
    except FileNotFoundError:
        return False

import pickle


def saveObjectOnPickle(obj, fileName):
    try:
        pickle.dump(obj, open(f'{fileName}.pkl', 'wb'))
        return True
    except pickle.PickleError:
        return False


def getObjectFromPickle(fileName):
    try:
        obj = pickle.load(open(f'{fileName}.pkl', 'rb'))
        return obj
    except pickle.PickleError:
        return False

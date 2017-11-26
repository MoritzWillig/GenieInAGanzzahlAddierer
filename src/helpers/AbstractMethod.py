
def AbstractMethod(func):
    def wrapper(self, **args):
        raise NotImplementedError(self.__class__.__name__, func.__name__)
    return wrapper
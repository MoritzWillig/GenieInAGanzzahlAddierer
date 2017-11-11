
def AbstractMethod(func):
    def wrapper():
        raise NotImplementedError(func.__name__)
    return wrapper
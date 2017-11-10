
def AbstractMethod(func):
    def wrapper():
        raise NotImplementedError(func.__name__)
    return wrapper

class GenieInterface(object):

    def __init__(self):
        None

    @AbstractMethod
    def get_inputs(self):
        None

    @AbstractMethod
    def get_outputs(self):
        None

    @AbstractMethod
    def serve(self, input):
        '''
        :param input:
        :return: Promise
        '''
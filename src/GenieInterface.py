from .helpers import AbstractMethod


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
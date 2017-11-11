from .helpers.AbstractMethod import AbstractMethod


class GenieInterface(object):

    def __init__(self, configuration):
        self._configuration = configuration

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

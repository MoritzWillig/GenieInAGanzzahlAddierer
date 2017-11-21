from ..helpers.AbstractMethod import AbstractMethod


class DataInstance(object):

    def __init__(self, type):
        self._type = type

    def get_type(self):
        return self._type

    @AbstractMethod
    def get_value(self):
        pass

    @AbstractMethod
    def serialize(self):
        pass

    @AbstractMethod
    def destroy(self):
        pass

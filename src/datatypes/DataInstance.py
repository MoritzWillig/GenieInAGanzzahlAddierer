from ..helpers.AbstractMethod import AbstractMethod

class DataInstance(object):

    def __init__(self, type):
        self._type = type

    def get_type(self):
        return self._type

    @AbstractMethod
    def get_value(self):
        None

    @AbstractMethod
    def serialize(self):
        None

    @AbstractMethod
    def deserialize(self, str):
        None

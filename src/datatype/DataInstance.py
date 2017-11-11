from ..helpers import AbstractMethod

class DataInstance(object):

    def __init__(self, type):
        None

    @AbstractMethod
    def get_type(self):
        None

    @AbstractMethod
    def serialize(self):
        None

    @AbstractMethod
    def deserialize(self):
        None

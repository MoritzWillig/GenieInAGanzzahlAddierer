from ..DataType import DataType
from .IntInstance import IntInstance


class IntType(DataType):

    def __init__(self):
        super().__init__()
        pass

    def get_name(self):
        return "integer"

    def create_instance(self):
        return IntInstance(self)

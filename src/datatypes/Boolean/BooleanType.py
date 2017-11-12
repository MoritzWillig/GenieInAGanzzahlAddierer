from ..DataType import DataType
from .BooleanInstance import BooleanInstance


class BooleanType(DataType):

    def __init__(self):
        super().__init__()
        pass

    def get_name(self):
        return "boolean"

    def create_instance(self):
        return BooleanInstance(self)

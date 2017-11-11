from .. import DataType
from . import IntInstance


class IntType(DataType):

    def __init__(self):
        None

    def get_name(self):
        return "integer"

    def create_instance(self):
        return IntInstance(self)

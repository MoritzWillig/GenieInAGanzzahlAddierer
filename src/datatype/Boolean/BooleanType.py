from .. import DataType
from . import BooleanInstance

class BooleanType(DataType):

    def __init__(self):
        None

    def get_name(self):
        return "boolean"

    def create_instance(self):
        return BooleanInstance(self)

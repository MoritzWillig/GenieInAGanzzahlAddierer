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

    def create_instance_with_value(self, value):
        instance = self.create_instance()
        instance.set_value(value)

    def create_instance_with_config(self, value_str, config):
        if value_str is not None:
            value = int(value_str)
        else:
            value = int(config["default"])

        return self.create_instance_with_value(value)

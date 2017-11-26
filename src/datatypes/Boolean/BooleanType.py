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

    def create_instance_with_value(self, value):
        instance = self.create_instance()
        instance.set_value(value)
        return instance

    def create_instance_with_config(self, value_str, config):
        if value_str is not None:
            value_str = value_str.lower()
            if value_str == "true":
                value = True
            elif value_str == "false":
                value = False
            else:
                raise Exception("Invalid boolean string")
        else:
            value = config["default"]
            if not isinstance(value, bool):
                raise Exception("Default value is not boolean")

        return self.create_instance_with_value(value)

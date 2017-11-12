from ..DataInstance import DataInstance

class BooleanInstance(DataInstance):

    def __init__(self, type):
        super(BooleanInstance, self).__init__(type)
        self._value = False

    def get_value(self):
        return self._value

    def serialize(self):
        return str(self._value)

    def deserialize(self, value_str):
        if value_str == "True":
            self._value = True
        elif value_str == "False":
            self._value = False
        else:
            raise Exception("Invalid boolean string")


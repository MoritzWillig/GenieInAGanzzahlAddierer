from ..DataInstance import DataInstance

class BooleanInstance(DataInstance):

    def __init__(self, type):
        super(BooleanInstance, self).__init__(type)
        self._value = False

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def serialize(self):
        return str(self._value)

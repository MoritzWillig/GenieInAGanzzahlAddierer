from ..DataInstance import DataInstance


class IntInstance(DataInstance):

    def __init__(self, type):
        super(IntInstance, self).__init__(type)
        self._value = 0

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def serialize(self):
        return str(self._value)


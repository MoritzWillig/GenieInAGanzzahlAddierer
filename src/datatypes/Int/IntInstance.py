from ..DataInstance import DataInstance
from ..DataInstance import Persistence


class IntInstance(DataInstance):

    def __init__(self, type, persistence=Persistence.SESSION):
        super(IntInstance, self).__init__(type, persistence)
        self._value = 0

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    def serialize_symbolic(self, attributes):
        return str(self._value)

    def _do_destroy(self):
        # nothing to do
        pass


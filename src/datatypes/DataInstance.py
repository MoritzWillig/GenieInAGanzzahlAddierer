from ..helpers.AbstractMethod import AbstractMethod
from enum import Enum


class Persistence(Enum):
    SESSION = 1
    PERMANENT = 2


class DataInstance(object):

    def __init__(self, type, persistence=Persistence.SESSION):
        self._type = type
        self._persistence = persistence

    def get_type(self):
        return self._type

    @AbstractMethod
    def get_value(self):
        pass

    @AbstractMethod
    def serialize_symbolic(self, attributes):
        """
        Returns a symbolic value for the data instance.
        For value types this is the value itself. For reference types
        it can be an path identifier. (e.g. the file path / url to an
        image, rather than the image data itself)
        :return: symbolic value
        :rtype: str
        """
        pass

    @AbstractMethod
    def _do_destroy(self):
        pass

    def destroy(self):
        if self._persistence != Persistence.PERMANENT:
            self._do_destroy()

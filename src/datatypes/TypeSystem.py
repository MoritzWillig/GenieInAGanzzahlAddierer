
class TypeSystem(object):

    def __init__(self):
        self._types = {}

    def register_type(self, name, type):
        self._types[name] = type

    def get_type_by_name(self, name):
        return self._types[name]

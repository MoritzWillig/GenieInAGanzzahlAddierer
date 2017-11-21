
class TypeSystem(object):

    def __init__(self):
        self._types = {}

    def register_type(self, name, type):
        self._types[name] = type

    def get_type_by_name(self, name):
        """
        :param name: name of a registered DataType
        :return: data type registered under the name
        :rtype: DataType
        """
        return self._types[name]

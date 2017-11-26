from .DataInstance import DataInstance

class InstanceScope(object):

    def __init__(self, typeSystem):
        self._typeSystem = typeSystem
        self._instances = {}

    def createInstance(self, name, args):
        raise Exception("Not implemented")
        instance = self._typeSystem.get_type_by_name(name).create_instance()
        self._instances.append(instance)
        return instance

    def addInstance(self, name, instance):
        if not isinstance(instance, DataInstance):
            raise Exception("object is no DataInstance")
        if not isinstance(name, str):
            raise Exception("name is no string")
        self._instances[name] = instance

    def getByName(self, name):
        return self._instances[name]

    def destroy(self):
        exceptions = []
        for instance in self._instances.values():
            try:
                instance.destroy()
            except Exception as e:
                exceptions.append(e)

        if len(exceptions) != 0:
            # TODO create nested exception
            raise Exception("Exception while destroying scope",exceptions)

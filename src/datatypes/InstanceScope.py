
class InstanceScope(object):

    def __init__(self, typeSystem):
        self._typeSystem = typeSystem
        self._instances = []

    def getInstance(self, name, args):
        instance = self._typeSystem.get_type_by_name(name).create_instance()
        self._instances.append(instance)
        return instance

    def destroy(self):
        exceptions = []
        for instance in self._instances:
            try:
                instance.destroy()
            except Exception as e:
                exceptions.append(e)

        if len(exceptions) != 0:
            # TODO create nested exception
            raise Exception("Exception while destroying scope",exceptions)

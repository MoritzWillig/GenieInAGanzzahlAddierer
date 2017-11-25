from ..DataInstance import DataInstance


class ImageInstance(DataInstance):

    def __init__(self, type, temp_file_manager):
        super(ImageInstance, self).__init__(type)
        self._temp_file_manager = temp_file_manager
        self._fileName = None
        self._owned = False

    def get_value(self):
        raise Exception("not implemented")

    def set_value(self, value, owned):
        self._fileName = value
        self._owned = owned

    def serialize(self):
        raise Exception("not implemented")

    def destroy(self):
        if self._fileName is not None and self._owned:
            self._temp_file_manager.deleteFile(self._fileName)

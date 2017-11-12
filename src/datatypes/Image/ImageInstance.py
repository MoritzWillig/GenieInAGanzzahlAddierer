from ..DataInstance import DataInstance


class ImageInstance(DataInstance):

    def __init__(self, type, temp_file_manager):
        super(ImageInstance, self).__init__(type)
        self._temp_file_manager = temp_file_manager
        self._fileName = None

    def get_value(self):
        raise Exception("not implemented")

    def serialize(self):
        raise Exception("not implemented")

    def deserialize(self, value_str):
        raise Exception("not implemented")

    def destroy(self):
        if self._fileName is not None:
            self._temp_file_manager.deleteFile(self._fileName)

from ..DataInstance import DataInstance
from ..DataInstance import Persistance


class ImageInstance(DataInstance):

    def __init__(self, type, temp_file_manager, persistance=Persistance.SESSION):
        super(ImageInstance, self).__init__(type, persistance)
        self._temp_file_manager = temp_file_manager
        self._fileName = None
        self._owned = False

    def get_value(self):
        raise Exception("not implemented")

    def set_value(self, value, owned=None):
        self._fileName = value
        if owned is not None:
            self._owned = owned

    def serialize_symbolic(self):
        return self._fileName

    def _do_destroy(self):
        if self._fileName is not None and self._owned:
            self._temp_file_manager.deleteFile(self._fileName)

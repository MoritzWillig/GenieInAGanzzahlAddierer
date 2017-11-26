from ..DataInstance import DataInstance
from ..DataInstance import Persistance


class ImageFolderInstance(DataInstance):

    def __init__(self, type, temp_file_manager, persistance=Persistance.SESSION):
        super(ImageFolderInstance, self).__init__(type, persistance)
        self._temp_file_manager = temp_file_manager
        self._folderName = None
        self._owned = False

    def get_value(self):
        raise Exception("not implemented")

    def set_value(self, value, owned=None):
        self._folderName = value
        if owned is not None:
            self._owned = owned

    def serialize_symbolic(self):
        return self._folderName

    def _do_destroy(self):
        if self._folderName is not None and self._owned:
            self._temp_file_manager.deleteFolder(self._folderName)

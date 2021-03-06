from src.datatypes.ScopeInfo import ScopeInfo
from ..DataInstance import DataInstance
from ..DataInstance import Persistence
import os

class ImageFolderInstance(DataInstance):

    def __init__(self, type, temp_file_manager, persistence=Persistence.SESSION):
        super(ImageFolderInstance, self).__init__(type, persistence)
        self._temp_file_manager = temp_file_manager
        self._folderName = None
        self._owned = False

    def get_value(self):
        raise Exception("not implemented")

    def set_value(self, value, owned=None):
        self._folderName = value
        if owned is not None:
            self._owned = owned

    def serialize_symbolic(self, attributes):
        scope = ScopeInfo.NAME if "scope" not in attributes else ScopeInfo.from_string(attributes["scope"])

        if scope == ScopeInfo.NAME:
            return self._folderName
        elif scope == ScopeInfo.FILE_PATH:
            return self._temp_file_manager.get_path_from_name(self._folderName)
        elif scope == ScopeInfo.URI:
            raise NotImplementedError("")
        else:
            raise RuntimeError("not reachable")

    def get_path(self):
        return self._temp_file_manager.get_path_from_name(self._folderName)

    def get_folder_name(self):
        path = self.get_path()
        if path[-1] == "/":
            path = path[:-1]
        return os.path.basename(path)

    def _do_destroy(self):
        if self._folderName is not None and self._owned:
            self._temp_file_manager.deleteFolder(self._folderName)

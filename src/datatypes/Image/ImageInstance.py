from src.datatypes.ScopeInfo import ScopeInfo
from ..DataInstance import DataInstance
from ..DataInstance import Persistence


class ImageInstance(DataInstance):

    def __init__(self, type, temp_file_manager, persistence=Persistence.SESSION):
        super(ImageInstance, self).__init__(type, persistence)
        self._temp_file_manager = temp_file_manager
        self._fileName = None
        self._owned = False

    def get_value(self):
        raise Exception("not implemented")

    def set_value(self, value, owned=None):
        self._fileName = value
        if owned is not None:
            self._owned = owned

    def serialize_symbolic(self, attributes):
        scope = ScopeInfo.NAME if "scope" not in attributes else ScopeInfo.from_string(attributes["scope"])

        if scope == ScopeInfo.NAME:
            return self._fileName
        elif scope == ScopeInfo.FILE_PATH:
            return self._temp_file_manager.get_path_from_name(self._fileName)
        elif scope == ScopeInfo.URI:
            raise NotImplementedError("")
        else:
            raise RuntimeError("not reachable")

    def get_path(self):
        return self._temp_file_manager.get_path_from_name(self._fileName)

    def _do_destroy(self):
        if self._fileName is not None and self._owned:
            self._temp_file_manager.deleteFile(self._fileName)

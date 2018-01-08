import pathlib
import os
import shutil

from src.fileManager.FileManipluator import FileManipulator


class FolderManipulator(object):

    def __init__(self, path):
        self._path = path

    def get_path(self):
        return self._path

    def get_path_from_name(self, name):
        if ".." in name:
            raise RuntimeError("Invalid name", name)
        return self._path + "/" + name

    def get_file(self, name):
        path = self.get_path_from_name(name)
        return FileManipulator(path)

    def createFolder(self, name, exist_ok=True):
        path = self.get_path_from_name(name)
        pathlib.Path(path).mkdir(parents=False, exist_ok=exist_ok)

    def deleteFile(self, name):
        path = self.get_path_from_name(name)
        os.remove(path)

    def deleteFolder(self, name):
        path = self.get_path_from_name(name)
        shutil.rmtree(path, ignore_errors=True)

    def file_exists(self, name):
        path = self.get_path_from_name(name)
        return os.path.isfile(path)

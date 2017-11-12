import pathlib
import os
import string
from random import choice

class TempFileManager(object):

    def __init__(self, tempFolder, prefix_length = 5):
        self._prefix_length = prefix_length
        self._name_index = 0
        self._tempFolder = str(pathlib.Path(tempFolder).absolute())
        self._prepareTempFolder()

    def _prepareTempFolder(self):
        self._prefix = self.create_random_string(self._prefix_length)+"_"
        pathlib.Path(self._tempFolder).mkdir(parents=True, exist_ok=True)

    def create_random_string(self, length):
        return "".join(choice(string.ascii_letters + string.digits) for _ in range(length))

    def get_path_from_name(self, name):
        return self._tempFolder + "/" + self._prefix + name

    def reserveName(self):
        name = str(self._name_index)
        self._name_index += 1
        return name

    def createTempFile(self):
        name = self.reserveName()
        path = self.get_path_from_name(name)
        with pathlib.Path(path).open("x") as _: pass

    def createTempFolder(self):
        name = self.reserveName()
        path = self.get_path_from_name(name)
        pathlib.Path(path).mkdir(parents=False, exist_ok=False)
        return name

    def deleteFile(self, name):
        path = self.get_path_from_name(name)
        os.remove(path)

    def deleteFolder(self, name):
        path = self.get_path_from_name(name)
        os.rmdir(path)


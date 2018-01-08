import pathlib
import os
from pathlib import Path

class FileManipulator(object):

    def __init__(self, path):
        self._path = path

    def get_path(self):
        return self._path

    def create(self, contents=None):
        with pathlib.Path(self._path).open("w") as f:
            if contents is not None:
                f.write(contents)

    def delete(self):
        os.remove(self._path)

    def exists(self):
        return os.path.isfile(self._path)

    def set_contents(self, contents):
        return Path(self._path).write_text(contents)

    def get_contents(self):
        return Path(self._path).read_text()

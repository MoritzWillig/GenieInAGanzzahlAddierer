import pathlib
import string
from random import choice

class TempFileManager(object):

    def __init__(self, tempFolder):
        self._tempFolder = tempFolder
        self._prepareTempFolder()

    def _prepareTempFolder(self):
        self._prefix = "".join(choice(string.ascii_letters+string.digits) for _ in range(5))+"_"
        pathlib.Path(self._tempFolder).mkdir(parents=True, exist_ok=True)

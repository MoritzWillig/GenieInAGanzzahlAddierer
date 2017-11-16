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
        """
        sets up a temporary folder to store files and folders
        """
        self._prefix = self._create_random_string(self._prefix_length)+"_"
        pathlib.Path(self._tempFolder).mkdir(parents=True, exist_ok=True)

    def _create_random_string(self, length):
        """
        Generates a random string of a given length,
        :param length: length of the string
        :return: the generated string consisting of ascii letters and digits
        :rtype string
        """
        return "".join(choice(string.ascii_letters + string.digits) for _ in range(length))

    def get_temp_folder(self):
        """
        Gives the name of the folder where the manager stores files and folders
        :return: path to the folder
        :rtype string
        """
        return self._tempFolder

    def get_path_from_name(self, name):
        return self._tempFolder + "/" + name

    def reserveName(self):
        """
        Reserves a new unique name for a file or folder
        :return: the reserved name
        :rtype string
        """
        name = self._prefix + str(self._name_index)
        self._name_index += 1
        return name

    def createTempFile(self):
        """
        creates a new file
        :return: name of the file
        :rtype string
        """
        name = self.reserveName()
        path = self.get_path_from_name(name)
        with pathlib.Path(path).open("x") as _: pass
        return name

    def createTempFolder(self):
        """
        creates a new folder
        :return: name of the folder
        :rtype string
        """
        name = self.reserveName()
        path = self.get_path_from_name(name)
        pathlib.Path(path).mkdir(parents=False, exist_ok=False)
        return name

    def deleteFile(self, name):
        """
        Deletes a file
        :param name: name of the file
        """
        path = self.get_path_from_name(name)
        os.remove(path)

    def deleteFolder(self, name):
        """
        Deletes a folder
        :param name: name of the folder
        """
        path = self.get_path_from_name(name)
        os.rmdir(path)


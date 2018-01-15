import pathlib
import os
import string
import shutil
from random import choice

class TempFileManager(object):

    def __init__(self, config, parent=None):
        self._prefix_length = config.get("folder_prefix_length", 8)
        self._static_temp_name = self._get_argument(config, "static_temp_name")
        self._append_counter = self._get_argument(config, "append_counter")
        self._use_static_folder = self._get_argument(config, "use_static_folder")
        self._name_index = 0
        self._base_path = str(pathlib.Path(self._get_argument(config, "directory")).absolute()) + "/"
        self._sub_path = None
        self._parent = None
        self._prepare_temp_folder()

    @staticmethod
    def _get_argument(config, key):
        try:
            return config[key]
        except KeyError:
            raise RuntimeError("Required argument '"+key+"' not found in 'temp' configuration")

    def _prepare_temp_folder(self):
        """
        sets up a temporary folder to store files and folders
        """
        self._prefix = self._static_temp_name if self._use_static_folder else \
            self._create_random_string(self._prefix_length)+("_" if self._append_counter else "")
        pathlib.Path(self._base_path).mkdir(parents=True, exist_ok=True)

    def get_prefix(self):
        return self._prefix

    @staticmethod
    def _create_random_string(length):
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
        return self._base_path

    def get_path_from_name(self, name):
        if ".." in name:
            raise RuntimeError("Invalid name", name)
        return self._base_path + name

    def reserveName(self, additional=None):
        """
        Reserves a new unique name for a file or folder
        :param additional: additional string to add to the name
        :return: the reserved name
        :rtype string
        """
        name = self._prefix
        if self._append_counter:
            name += str(self._name_index)
        if additional is not None:
            name += additional

        self._name_index += 1
        return self._sub_path + name

    def createTempFile(self):
        """
        creates a new file
        :return: name of the file
        :rtype string
        """
        name = self.reserveName()
        path = self.get_path_from_name(name)
        with pathlib.Path(path).open("x") as _:
            pass
        return name

    def createTempFolder(self):
        """
        creates a new folder
        :return: name of the folder
        :rtype string
        """
        name = self.reserveName()
        path = self.get_path_from_name(name)

        # if a user specific folder without a counter is used, each request uses the same folder -> exist_ok=True
        # in all other cases, name collisions should be handled as errors  -> exist_ok=False
        exist_ok=self._use_static_folder and not self._append_counter

        pathlib.Path(path).mkdir(parents=False, exist_ok=exist_ok)
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
        Recursively deletes a folder
        :param name: name of the folder
        """
        path = self.get_path_from_name(name)
        shutil.rmtree(path, ignore_errors=True)

    def file_exists(self, name):
        path = self.get_path_from_name(name)
        return os.path.isfile(path)

    def set_sub_folder(self, sub_path):
        """
        Sets a sub path which will be prepended to all newly created names
        :param sub_path: string subpath to prepend
        """
        self._sub_path = sub_path

    def get_sub_folder(self):
        return self._sub_path

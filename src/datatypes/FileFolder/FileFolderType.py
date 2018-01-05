from src.datatypes.CreationInfo import CreationInfo
from src.datatypes.DataType import DataType
from src.datatypes.FileFolder.FileFolderInstance import FileFolderInstance


class FileFolderType(DataType):

    def __init__(self, temp_file_manager):
        super().__init__()
        self._temp_file_manager = temp_file_manager

    def get_name(self):
        return "image"

    def create_instance(self):
        return FileFolderInstance(self, self._temp_file_manager)

    def create_instance_with_value(self, value):
        instance = self.create_instance()
        instance.set_value(value, False)
        return instance

    def create_instance_with_config(self, value_str, config):
        create_info = CreationInfo.CREATE if "creation" not in config else CreationInfo.from_string(config["creation"])

        if create_info == CreationInfo.CREATE:
            name = self._temp_file_manager.createTempFolder()
            return self.create_instance_with_value(name)
        elif create_info == CreationInfo.RESERVE:
            name = self._temp_file_manager.reserveName()
            return self.create_instance_with_value(name)
        elif create_info == CreationInfo.EXISTING:
            path = self._temp_file_manager.get_path_from_name(value_str)
            return self.create_instance_with_value(path)
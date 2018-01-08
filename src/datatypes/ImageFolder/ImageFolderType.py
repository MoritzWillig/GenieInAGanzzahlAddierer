from ..DataType import DataType
from .ImageFolderInstance import ImageFolderInstance
from src.datatypes.CreationInfo import CreationInfo


class ImageFolderType(DataType):

    def __init__(self, temp_file_manager):
        super().__init__()
        self._temp_file_manager = temp_file_manager

    def get_name(self):
        return "image"

    def create_instance(self):
        return ImageFolderInstance(self, self._temp_file_manager)

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
            name = value_str
            return self.create_instance_with_value(name)

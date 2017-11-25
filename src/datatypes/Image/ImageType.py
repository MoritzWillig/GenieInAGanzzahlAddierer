from ..DataType import DataType
from .ImageInstance import ImageInstance


class ImageType(DataType):

    def __init__(self, temp_file_manager):
        super().__init__()
        self._temp_file_manager = temp_file_manager

    def get_name(self):
        return "image"

    def create_instance(self):
        return ImageInstance(self, self._temp_file_manager)

    def create_instance_with_value(self, value):
        instance = self.create_instance()
        instance.set_value(value, False)
        return instance

    def create_instance_with_config(self, value_str, config):
        create_new = False if "creation" in config and config["creation"] == "existing" else True

        if create_new:
            name = self._temp_file_manager.createTempFile()
            return self.create_instance_with_value(name)
        else:
            path = self._temp_file_manager.get_path_from_name(value_str)
            return self.create_instance_with_value(path)

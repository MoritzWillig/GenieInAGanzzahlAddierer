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

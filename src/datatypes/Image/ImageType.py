from .. import DataType
from . import ImageInstance

class ImageType(DataType):

    def __init__(self, tempFileManager):
        self._tempFileManager = tempFileManager

    def get_name(self):
        return "image"

    def create_instance(self):
        return ImageInstance(self, self._tempFileManager)

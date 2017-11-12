from .. import DataInstance

class ImageInstance(DataInstance):

    def __init__(self, type, tempFileManager):
        super(ImageInstance, self).__init__(type)

    def get_value(self):
        raise Exception("not implemented")

    def serialize(self):
        raise Exception("not implemented")

    def deserialize(self, value_str):
        raise Exception("not implemented")


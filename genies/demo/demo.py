from ...src import GenieInterface

class DemoGenie(GenieInterface):

    def __init__(self):
        None

    def get_inputs(self):
        return ["image", "image", "int"]

    def get_outputs(self):
        return ["image", "image", "image"]

    def serve(self, input):
        raise NotImplementedError("")

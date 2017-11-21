from src.GenieInterface import GenieInterface


class DemoGenie(GenieInterface):
    def __init__(self, configuration, additional):
        super(DemoGenie, self).__init__(configuration, additional)

    def get_inputs(self):
        return {"input1": "image", "input2": "image", "param": "int"}

    def get_outputs(self):
        return {"output1": "image", "output2": "image", "output3": "int"}

    def serve(self, input):
        raise NotImplementedError("D:")

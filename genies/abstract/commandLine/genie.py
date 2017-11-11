from ....src import GenieInterface
from ....src.helpers import AbstractMethod
from subprocess import call

class CommandLineGenie(GenieInterface):

    def __init__(self, configuration):
        self._configuration = configuration

    @AbstractMethod
    def get_inputs(self):
        return ["image", "image", "int"]

    @AbstractMethod
    def get_outputs(self):
        return ["image", "image", "image"]

    def _argument_to_string(self, arg):
        type = arg.type

        if type != "plain":
            raise Exception("only 'plain' arguments supported")

        result = arg.text

        if type(result) != "string":
            raise Exception("evaluated argument is no string")

        return result

    def _process_input_argument(self, arg, inputs):
        id = arg.id
        if type(id) == "string":
            raise Exception("input argument id is not a string")
        type = arg.type

        if type == "plain":
            raise Exception("plain is no input type")
        elif type == "image":
            # save image to temp
            # set value to image path
            raise Exception("Not implemented")
        elif type == "image_folder":
            raise Exception("image_folder is no input type")
        elif type == "int_range":
            raise Exception("Not implemented")
        elif type == "boolean":
            input = inputs.select_single_by_attribute("id",id)
            if input.get_type() != Boolean:
                raise Exception("Input is not Boolean")
            arg.type = "plain"
            arg.text = "True" if input.get_value() else "False"
        else:
            raise Exception("Unknown argument type")

    def _process_output_argument(self, arg, inputs):
        id = arg.id
        if type(id) == "string":
            raise Exception("input argument id is not a string")
        type = arg.type

        if type == "plain":
            raise Exception("plain is no output type")
        elif type == "image":
            # create unused temp name
            # set value to image path
            raise Exception("Not implemented")
        elif type == "image_folder":
            # create unused temp name
            # set value to image path
            raise Exception("Not implemented")
        elif type == "int_range":
            raise Exception("plain is no output type")
        elif type == "boolean":
            raise Exception("plain is no output type")
        else:
            raise Exception("Unknown argument type")

    def _build_command_line(self, inputs):
        wc = self._configuration.arguments.copy()

        inputs_ = wc.select_by_attribute("semantic","in")
        map(lambda arg: self._process_input_argument(arg, inputs), inputs_)
        outputs_ = wc.select_by_attribute("semantic","out")
        map(lambda arg: self._process_output_argument(arg, inputs), outputs_)

        str_arguments = map(lambda arg: self._argument_to_string(arg), wc)
        return " ".join(str_arguments)


    def serve(self, input):
        result = call(self._build_command_line(input))

        send result here ...

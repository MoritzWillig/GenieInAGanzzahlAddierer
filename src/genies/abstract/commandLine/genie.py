from src.GenieInterface import  GenieInterface
from src.helpers.AbstractMethod import AbstractMethod
from subprocess import call
from src.datatypes.Boolean import BooleanType
from src.datatypes.Int import IntType
import json


class CommandlineGenie(GenieInterface):

    def __init__(self, configuration, parameters, type_system):
        super(CommandlineGenie, self).__init__(configuration, parameters, type_system)

        _inputs = self._select_by_attribute(self._additional["arguments"], "semantic", "in")
        _outputs = self._select_by_attribute(self._additional["arguments"], "semantic", "out")

        _inputs_map = {}
        for input in _inputs:
            name = input["id"]
            type_str = input["type"]
            _inputs_map[name] = type_str

        _outputs_map = {}
        for output in _outputs:
            name = output["id"]
            type_str = output["type"]
            _outputs_map[name] = type_str

        self._inputs = _inputs_map
        self._outputs = _outputs_map

    def _select_by_attribute(self, data, name, value):
        result = []
        for item in data:
            if (name in item) and (item[name] == value):
                result.append(item)
        return result

    def _select_single_by_attribute(self, data, name, value):
        for item in data:
            if item[name] == value:
                return item
        raise RuntimeError("key not found")

    def get_inputs(self):
        return self._inputs

    def get_outputs(self):
        return self._outputs

    def _argument_to_string(self, arg):
        type = arg.type

        if type != "plain":
            raise Exception("only 'plain' arguments supported")

        result = arg.text

        if isinstance(result, str):
            raise Exception("evaluated argument is no string")

        return result

    def _process_input_argument(self, arg, inputs):
        id = arg.id
        if isinstance(id, str):
            raise Exception("input argument id is not a string")
        type = arg.type
        input = self._select_single_by_attribute(inputs, "id", id)

        if type == "plain":
            raise Exception("plain is no input type")
        elif type == "image":
            # save image to temp
            # set value to image path
            raise Exception("Not implemented")
        elif type == "image_folder":
            raise Exception("image_folder is no input type")
        elif type == "int_range":
            # result of an int_range is an int
            # FIXME modify IntType to allow range constraints
            if isinstance(input.get_type(), IntType):
                raise Exception("Input is not Int")
            arg.type = "plain"
            arg.text = input.serialize()
        elif type == "boolean":
            if isinstance(input.get_type(), BooleanType):
                raise Exception("Input is not Boolean")
            arg.type = "plain"
            arg.text = input.serialize()
        else:
            raise Exception("Unknown argument type")

    def _process_output_argument(self, arg, inputs):
        id = arg.id
        if isinstance(id,str):
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
            raise Exception("int_range is no output type")
        elif type == "boolean":
            raise Exception("plain is no output type")
        else:
            raise Exception("Unknown argument type")

    def _build_command_line(self, inputs):
        wc = self._additional["arguments"].copy()

        inputs_ = self._select_by_attribute(wc, "semantic","in")
        map(lambda arg: self._process_input_argument(arg, inputs), inputs_)
        outputs_ = self._select_by_attribute(wc, "semantic","out")
        map(lambda arg: self._process_output_argument(arg, inputs), outputs_)

        str_arguments = map(lambda arg: self._argument_to_string(arg), wc)
        return str_arguments

    def serve(self, input, scope):
        # result = call(self._build_command_line(input))
        return "Test"

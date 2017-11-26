from src.GenieInterface import  GenieInterface
from src.helpers.AbstractMethod import AbstractMethod
from subprocess import call
from src.datatypes.Boolean import BooleanType
from src.datatypes.Int import IntType
from src.datatypes.Image.ImageType import CreationInfo
import json
from collections import deque


class CommandlineGenie(GenieInterface):

    def __init__(self, configuration, parameters, type_system):
        super(CommandlineGenie, self).__init__(configuration, parameters, type_system)

        _inputs = self._select_by_attribute(self._additional["arguments"], "semantic", "in")
        _outputs = self._select_by_attribute(self._additional["arguments"], "semantic", "out")

        self._named_args = {}
        _inputs_map = {}
        for input in _inputs:
            name = input["id"]
            type_str = input["type"]
            _inputs_map[name] = type_str
            self._named_args[name] = input

        _outputs_map = {}
        for output in _outputs:
            name = output["id"]
            type_str = output["type"]
            _outputs_map[name] = type_str
            self._named_args[name] = output

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

    def get_config_for_input(self, name):
        return self._named_args[name]

    def get_inputs(self):
        return self._inputs

    def get_outputs(self):
        return self._outputs

    def _argument_to_string(self, arg):
        type = arg["type"]

        if type != "plain":
            raise Exception("only 'plain' arguments supported, but type was '"+type+"'")

        result = arg["text"]

        if not isinstance(result, str):
            raise Exception("evaluated argument is no string ")

        return result

    def _process_input_argument(self, arg, scope):
        id = arg['id']
        if not isinstance(id, str):
            raise Exception("input argument id is not a string")
        type = arg['type']

        instance = scope.getByName(id)

        config = {
            "scope": "filepath"
        }

        if type == "plain":
            raise Exception("plain is no input type")
        elif type == "image":
            # save image to temp
            # set value to image path
            arg['type'] = "plain"
            arg['text'] = instance.serialize_symbolic(config)
        elif type == "image_folder":
            raise Exception("image_folder is no input type")
        elif type == "int":
            arg['type'] = "plain"
            arg['text'] = instance.serialize_symbolic(config)
        elif type == "boolean":
            arg['type'] = "plain"
            arg['text'] = instance.serialize_symbolic(config)
        else:
            raise Exception("Unknown argument type")

    def _process_output_argument(self, arg, scope):
        # FIXME instances are not added to scope

        id = arg['id']
        if not isinstance(id,str):
            raise Exception("output argument id is not a string ")
        type = arg['type']

        config = {
            "scope": "filepath"
        }

        # create output instances
        # we currently only allow reference types as output
        if type == "plain":
            raise Exception("plain is no output type")
        elif type == "image":
            # resserve temp
            # set value to image path
            data_type = self._type_system.get_type_by_name("image")

            # if the creation info is not set explicitely by the user,
            # we reserve a name and expect to application to create the file
            if "creation" not in arg:
                arg["creation"] = CreationInfo.to_string(CreationInfo.RESERVE)
            instance = data_type.create_instance_with_config("", arg)
        elif type == "image_folder":
            # create temp folder
            data_type = self._type_system.get_type_by_name("image_folder")
            instance = data_type.create_instance_with_config("", arg)
        elif type == "int":
            raise Exception("int is no output type")
        elif type == "boolean":
            raise Exception("boolean is no output type")
        else:
            raise Exception("Unknown argument type")

        # convert to plain
        arg['type'] = "plain"
        arg['text'] = instance.serialize_symbolic(config)

    def _build_command_line(self, inputs, scope):
        wc = self._additional["arguments"].copy()

        inputs_ = self._select_by_attribute(wc, "semantic", "in")
        deque(map(lambda arg: self._process_input_argument(arg, scope), inputs_))
        outputs_ = self._select_by_attribute(wc, "semantic", "out")
        deque(map(lambda arg: self._process_output_argument(arg, scope), outputs_))

        str_arguments = list(map(lambda arg: self._argument_to_string(arg), wc))
        return str_arguments

    def serve(self, input, scope):
        # result = call(self._build_command_line(input, scope))
        return self._build_command_line(input, scope)

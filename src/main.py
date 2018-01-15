from flask import Flask, send_from_directory, request, jsonify
import importlib
from os import listdir
from os.path import isfile, join
import json
import re

from src.datatypes.CreationInfo import CreationInfo
from src.datatypes.FileFolder.FileFolderType import FileFolderType
from src.fileManager.FolderManipulator import FolderManipulator
from src.fileManager.TempFileManager import TempFileManager
from src.datatypes.TypeSystem import TypeSystem
from src.datatypes.Int.IntType import IntType
from src.datatypes.Boolean.BooleanType import BooleanType
from src.datatypes.Image.ImageType import ImageType
from src.datatypes.ImageFolder.ImageFolderType import ImageFolderType
from src.datatypes.InstanceScope import InstanceScope


class Genie(object):
    def __init__(self, name):
        self._loadConfig()

        self._tempFileManager = TempFileManager(self._config["temp"])
        self._runtime_cfg = {
            "session": {
                #we currently use the prefix as session name. if results are grouped by session
                #a folder should be created for each session TODO
                "name": self._tempFileManager.get_prefix()
            }
        }
        self._config["_runtime"] = self._runtime_cfg
        self._setup_type_system()

        self._genies = {}

        for genie_cfg in self._config['genies']:
            if ("ignore" in genie_cfg) and genie_cfg["ignore"] is True:
                continue

            _, genie = self._load_genie(genie_cfg['genie'])
            genie_additional_cfg = \
                None if 'configuration' not in genie_cfg else self._loadGenieConfig(genie_cfg['configuration'])
            genie_instance = genie(self._config, genie_additional_cfg, self._type_system)
            self.registerGenie(genie_cfg['name'], genie_instance)

        self.app = Flask(name, static_url_path='')
        self.app.debug = True

        @self.app.route("/")
        def serve_index():
            return send_from_directory('static', 'index.html')

        @self.app.route('/genie/<genie_name>/interface')
        def server_genie_interface(genie_name):
            if genie_name not in self._genies:
                return jsonify({"success": False, "error": 'Unknown genie.'})

            genie = self._genies[genie_name]
            return jsonify({
                "inputs": genie.get_inputs(),
                "outputs:": genie.get_outputs()
            })

        @self.app.route('/genie/<genie_name>/request/<session_name>', methods=["GET"])
        def serve_genie_request(genie_name, session_name):
            if request.method != 'GET':
                return jsonify({"success": False, "error": 'Invalid request.'})

            session_folder = _load_session(session_name)
            if session_folder is None:
                return jsonify({"success": False, "message": "session does not exist"})

            session_sub_folder = self._tempFileManager.get_sub_folder()

            # load session info
            session_file = session_folder.get_file("session_info.json")
            contents = session_file.get_contents()
            session_object = json.loads(contents)
            if not isinstance(session_object, dict):
                return jsonify({"success": False, "message": "could not read session information"})

            # TODO validate correct session_object structure
            value_inputs = request.args
            file_inputs = session_object["inputs"]["mapping"]

            if genie_name not in self._genies:
                return jsonify({"success": False, "error": 'unknown genie.'})

            genie = self._genies[genie_name]
            inputs = genie.get_inputs()
            outputs = genie.get_outputs()

            # check for correct inputs
            try:
                args = {}
                for input_name in inputs.keys():
                    if input_name in value_inputs:
                        args[input_name] = value_inputs[input_name]
                    elif input_name in file_inputs:
                        args[input_name] = file_inputs[input_name]
                    else:
                        raise RuntimeError("required argument '"+input_name+"' was not provided")
            except RuntimeError as e:
                return jsonify({"success": False, "error": 'parameters do not match.', "message":str(e)})

            # create a new scope for this request
            variable_scope = InstanceScope(self._type_system)

            # convert each arguments string into a type instance
            try:
                # all input files are stored in the "inputs" folder of the session
                self._tempFileManager.set_sub_folder(session_sub_folder + "inputs/")

                for arg_name, arg_value_str in args.items():
                    config = genie.get_config_for_input(arg_name)
                    # all inputs are assumed to already exist. If the user
                    # does not explicitly specify otherwise creation information
                    # is set to EXISTING
                    if "creation" not in config:
                        config["creation"] = CreationInfo.to_string(CreationInfo.EXISTING)

                    data_type = self._type_system.get_type_by_name(inputs[arg_name])
                    instance = data_type.create_instance_with_config(
                        arg_value_str, config)
                    variable_scope.addInstance(arg_name, instance)
            except Exception as e:
                variable_scope.destroy()
                raise e
                return jsonify({"success": False, "error": 'Invalid inputs'})
            self._tempFileManager.set_sub_folder(session_sub_folder)

            try:
                # all files created by the genie should be stored in the outputs directory
                self._tempFileManager.set_sub_folder(session_sub_folder + "outputs/")
                response = genie.serve(inputs, variable_scope)
                variable_scope.destroy()
                return jsonify({"success": True, "response": response})
            except Exception as e:
                variable_scope.destroy()
                raise e
                return jsonify({"success": False, "error": 'Genie failed'})
            self._tempFileManager.set_sub_folder(session_sub_folder)


            variable_scope.destroy()
            raise RuntimeError("Unreachable")

        def _get_folder_from_session(session_name):
            # if ("." in session_name) or ("/" in session_name):
            if re.match("[A-Za-z0-9]+$", session_name):
                return None
            return session_name

        def _load_session(session_name):
            config = {"creation": CreationInfo.to_string(CreationInfo.EXISTING)}
            data_type = self._type_system.get_type_by_name("file_folder")
            folder_name = _get_folder_from_session(session_name)
            # check for invalid session_name
            if folder_name is None:
                return None
            instance = data_type.create_instance_with_config(folder_name, config)

            # change _tempFileManager path to session folder
            self._tempFileManager.set_sub_folder(folder_name + "/")

            if not instance.exists():
                return None

            folder = FolderManipulator(instance.get_path())
            return folder

        @self.app.route('/session/create', methods=["GET"])
        def serve_session_create():
            config = {"creation": CreationInfo.to_string(CreationInfo.CREATE)}
            data_type = self._type_system.get_type_by_name("file_folder")
            instance = data_type.create_instance_with_config(None, config)

            session_name = instance.get_value()
            session_folder = _load_session(session_name)
            if session_folder is None:
                return jsonify({"success": False, "message": "session could not be created"})

            session_folder.createFolder("inputs")
            session_folder.createFolder("outputs")
            session_file = session_folder.get_file("session_info.json")
            session_file.set_contents(json.dumps({
                "inputs": {
                    "count": 0,
                    "mapping": {}
                },
                "information": {
                    "status": "created"
                }
            }))

            return jsonify({"success": True, "session": session_name})

        @self.app.route('/session/<session_name>/upload/<input_id>', methods=["GET", "POST"])
        def serve_session_upload(session_name, input_id):
            session_folder = _load_session(session_name)
            if session_folder is None:
                return jsonify({"success": False, "message": "session does not exist"})

            session_sub_folder = self._tempFileManager.get_sub_folder()

            # load session info
            session_file = session_folder.get_file("session_info.json")
            contents = session_file.get_contents()
            session_object = json.loads(contents)
            if not isinstance(session_object, dict):
                return jsonify({"success": False, "message": "could not read session information"})

            #TODO validate correct session_object structure
            inputs = session_object["inputs"]

            # store input files
            # FIXME implement (configurable) upload limit/constraints
            for file in request.files.getlist('file'):
                if input_id in inputs["mapping"].keys():
                    #TODO allow overwriting input ids
                    raise RuntimeError("Input id '"+input_id+"' was already uploaded")

                self._tempFileManager.set_sub_folder(session_sub_folder + "input/")
                # add session counter to name to prevent name clashes on server restart
                # TODO _tempFileManager should save counters per directory
                filename = self._tempFileManager.reserveName("_"+str(inputs["count"]))
                filepath = session_folder.get_path_from_name(filename)
                file.save(filepath)

                inputs["count"] += 1
                inputs["mapping"][input_id] = filename

            # save uploaded files to session information
            session_file.set_contents(json.dumps(session_object))

            return jsonify({"success": True, "message": "ok"})

        @self.app.route('/session/<session_name>/status', methods=["GET"])
        def serve_session_status(session_name):
            #FIXME
            raise NotImplementedError("Not implemented")

        @self.app.route('/session/<session_name>/serve/<data_id>', methods=["GET"])
        def serve_session_result_output(session_name, data_id):
            folder_name = _get_folder_from_session(session_name)
            if folder_name is None:
                return jsonify({"success": False, "message": "session does not exist"})
            return send_from_directory(self._tempFileManager.get_temp_folder() + "/" + folder_name + "/" + "outputs/", data_id)

        def valid_file_extension(filename):
            ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
            return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

        if ("dev" in self._config) and ("enable" in self._config["dev"]) and self._config["dev"]["enable"] is True:
            print("dev mode enabled - serving dev files")

            @self.app.route('/dev/upload_tester/')
            @self.app.route('/dev/upload_tester/<path:path>')
            def upload_tester(path=None):
                if path is None:
                    path = "index.html"
                return send_from_directory("./static/dev/", path)

    def _loadGenieConfig(self, config_path):
        with open(config_path) as f:
            config_str = f.read()
        return json.loads(config_str)

    def _load_genie(self, name_path):
        """
        loads a Genie module from the .genies directory
        :param name_path: name of the genie directory
        :type name_path: string
        :return: Genie class
        :rtype: string, .genies.GenieInterface
        """
        path = ".genies."+name_path+".genie"
        module = importlib.import_module(path, __package__)

        name = name_path.rsplit(".",1)[1] if "." in name_path else name_path
        genieName = name.capitalize()+"Genie"
        genie = module.__dict__[genieName]
        return genieName, genie

    def _loadConfig(self):
        with open("./config.json") as f:
            config_str = f.read()
        self._config = json.loads(config_str)
        self._config['__master'] = self

    def _setup_type_system(self):
        self._type_system = TypeSystem()
        self._type_system.register_type("int", IntType())
        self._type_system.register_type("boolean", BooleanType())
        self._type_system.register_type("image", ImageType(self._tempFileManager))
        self._type_system.register_type("image_folder", ImageFolderType(self._tempFileManager))
        self._type_system.register_type("file_folder", FileFolderType(self._tempFileManager))


    def registerGenie(self, name, genie):
        """
        registeres a Genie at the api interface
        :param name: genie name
        :type name: string
        :param genie: genie instance
        :type name: Genie
        """
        self._genies[name] = genie

    def serve(self):
        self.app.run()

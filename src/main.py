from flask import Flask, send_from_directory, request, jsonify
import importlib
import json
from os import listdir
from os.path import isfile, join

from src.fileManager.TempFileManager import TempFileManager
from src.datatypes.TypeSystem import TypeSystem
from src.datatypes.Int.IntType import IntType
from src.datatypes.Boolean.BooleanType import BooleanType
from src.datatypes.Image.ImageType import ImageType
from src.datatypes.InstanceScope import InstanceScope


class Genie(object):
    def __init__(self, name):
        self._loadConfig()

        self._genies={}

        for genie_cfg in self._config['genies']:
            if ("ignore" in genie_cfg) and genie_cfg["ignore"]==True:
                continue

            _, genie = self._load_genie(genie_cfg['genie'])
            self.registerGenie(genie_cfg['name'], genie(self._config, genie_cfg['configuration']))

        self._tempFileManager = TempFileManager(self._config["temp"], 8)

        self._setup_type_system()

        self.app = Flask(name, static_url_path='')
        self.app.debug = True

        @self.app.route("/")
        def serve_index():
            return send_from_directory('static', 'index.html')

        @self.app.route('/genie/<genie_name>/interface')
        def server_genie_interface(genie_name):
            if genie_name not in self._genies:
                return jsonify({"success": False, "error": 'Unknown genie.'})

            return jsonify({"success": False, "error": 'Not implemented.'})

        @self.app.route('/genie/<genie_name>/request', methods=["GET"])
        def serve_genie_request(genie_name):
            if request.method != 'GET':
                return jsonify({"success": False, "error": 'Invalid request method.'})

            if genie_name not in self._genies:
                return jsonify({"success": False, "error": 'Unknown genie.'})

            genie = self._genies[genie_name]
            inputs = genie.get_inputs()
            outputs = genie.get_outputs()

            # check for correct inputs
            try:
                args = self._filter_superset(request.args, inputs.keys()) # Dict{string, string}
            except RuntimeError as e:
                return jsonify({"success": False, "error": 'Parameters do not match.'})

            # create a new scope for this request
            variable_scope = InstanceScope(self._type_system)

            # convert each arguments string into a type instance
            try:
                for arg_name, arg_value_str in args.items():
                    data_type = self._type_system.get_type_by_name(inputs[arg_name])
                    instance = data_type.create_instance_with_config(
                        arg_value_str, genie.get_config_for_input(arg_name))
                    variable_scope.addInstance(instance)
            except Exception as e:
                variable_scope.destroy()
                return jsonify({"success": False, "error": 'Genie failed'})

            try:
                response = genie.serve(inputs)
            except Exception as e:
                variable_scope.destroy()
                return jsonify({"success": False, "error": 'Genie failed'})

            variable_scope.destroy()
            return jsonify({"success": False, "msg": response})

        @self.app.route('/upload', methods=['POST'])
        def upload():
            if request.method != 'POST':
                return jsonify({"success": False, "error": 'Invalid request method.'})

            filename = None # store filename of last file
            for file in request.files.getlist('file'):
                if not file or not valid_file_extension(file.filename):
                    return jsonify({"success": False, "error": 'Invalid file type.'})
                else:
                    filename = self._tempFileManager.createTempFile()
                    filepath = self._tempFileManager.get_path_from_name(filename)
                    file.save(filepath)

            return jsonify({"success": True, "filename": filename})

        def valid_file_extension(filename):
            ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
            return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

        @self.app.route('/api/get/uploads.json')
        def get_upload_list():
            temp_dir = self._tempFileManager.get_temp_folder()
            return jsonify({'files': [f for f in listdir(temp_dir) if isfile(join(temp_dir, f))]})

        @self.app.route('/uploads/<path:path>')
        def send_images(path):
            return send_from_directory(self._tempFileManager.get_temp_folder(), path)

    def _filter_superset(self, superset, subset):
        """
        checks if all keys contained in subset are present in the superset
        :param superset:  request.arg
        :type superset:   Dict{string, Any}
        :param subset:    name of input parameters
        :type subset: Enum{string}
        :return: dict of matching superset objects
        :rtype: Dict{string, string}
        """
        parameters={}

        for sub in subset:
            value = superset.get(sub)

            if value is None:
                raise RuntimeError("key does not exist in superset")

            parameters[sub] = value

        return parameters

    def _load_genie(self, name):
        """
        loads a Genie module from the .genies directory
        :param name: name of the genie directory
        :type name: string
        :return: Genie class
        :rtype: string, .genies.GenieInterface
        """
        path = ".genies."+name+".genie"
        module = importlib.import_module(path, __package__)
        genieName = name.capitalize()+"Genie"
        genie = module.__dict__[genieName]
        return genieName, genie

    def _loadConfig(self):
        with open("./config.json") as f:
            config_str = f.read()
        self._config = json.loads(config_str)
        self._config['__master']=self

    def _setup_type_system(self):
        self._type_system = TypeSystem()
        self._type_system.register_type("int", IntType())
        self._type_system.register_type("boolean", BooleanType())
        self._type_system.register_type("image", ImageType(self._tempFileManager))

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

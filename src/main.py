from datetime import datetime
from flask import Flask, send_from_directory, request, jsonify
import importlib
import json
import os

from src.fileManager.TempFileManager import TempFileManager
from src.datatypes.TypeSystem import TypeSystem
from src.datatypes.Int.IntType import IntType
from src.datatypes.Boolean.BooleanType import BooleanType
from src.datatypes.Image.ImageType import ImageType


class Genie(object):
    def __init__(self, name):
        self._loadConfig()

        self._genies={}
        for genie_str in self._config['genies']:
            genieName, genie = self._load_genie(genie_str)
            self.registerGenie(name, genie(self._config))

        self._tempFileManager = TempFileManager(self._config["temp"])

        self._setup_type_system()

        self.app = Flask(name, static_url_path='')
        self.app.debug = True

        @self.app.route("/")
        def serve_index():
            return send_from_directory('static', 'index.html')

        @self.app.route('/genie/<path:path>')
        def serve_genie():
            raise Exception("Not implemented")

        @self.app.route('/content/<path:path>')
        def serve_static(path):
            return send_from_directory('content', path)

        @self.app.route('/upload', methods=['POST'])
        def upload():
            if request.method != 'POST':
                return jsonify({"success": False, "error": 'Invalid request method.'})

            filename = None # store filename of last file
            for file in request.files.getlist('file'):
                if not file or not valid_file_extension(file.filename):
                    return jsonify({"success": False, "error": 'Invalid file type.'})
                else:
                    now = datetime.now()
                    filename = os.path.join("%s.%s" % (now.strftime("%Y-%m-%d-%H-%M-%S-%f"), file.filename.rsplit('.', 1)[1]))
                    filepath = os.path.join('uploads', filename)
                    file.save(filepath)

            return jsonify({"success": True, "filename": filename})

        def valid_file_extension(filename):
            ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
            return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

        @self.app.route('/uploads/<path:path>')
        def send_images(path):
            return send_from_directory('uploads', path)

    def _load_genie(self, name):
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
        self._typeSystem = TypeSystem()
        self._typeSystem.register_type("int", IntType())
        self._typeSystem.register_type("boolean", BooleanType())
        self._typeSystem.register_type("image", ImageType(self._tempFileManager))

    def registerGenie(self, name, genie):
        self._genies[name] = genie

    def serve(self):
        self.app.run()

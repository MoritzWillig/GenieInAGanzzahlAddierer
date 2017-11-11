from flask import Flask, send_from_directory
import json
import importlib

class Genie(object):
    def __init__(self, name):
        self._loadConfig()

        self._genies={}
        for genie_str in self._config['genies']:
            genieName, genie = self._load_genie(genie_str)
            self.registerGenie(name, genie(self._config))
        temp = self._config["temp"] # "./temp"


        self.app = Flask(name, static_url_path='')

        @self.app.route("/")
        def serve_index():
            return send_from_directory('clientside/pages', 'index.html')

        @self.app.route('/genie/<path:path>')
        def serve_genie():
            raise Exception("Not implemented")

        @self.app.route('/content/<path:path>')
        def serve_static(path):
            return send_from_directory('content', path)

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

    def registerGenie(self, name, genie):
        self._genies[name] = genie

    def serve(self):
        self.app.run()

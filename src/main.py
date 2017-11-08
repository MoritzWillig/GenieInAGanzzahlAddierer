from flask import Flask

class Genie(object):

    def __init__(self, name):
        self.app = Flask(name)

        @self.app.route("/")
        def hello():
            return "Hello World!"

    def serve(self):
        self.app.run()
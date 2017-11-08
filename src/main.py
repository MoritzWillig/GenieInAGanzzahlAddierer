from flask import Flask, send_from_directory


class Genie(object):
    def __init__(self, name):
        self.app = Flask(name, static_url_path='')

        @self.app.route("/")
        def serve_index():
            return send_from_directory('clientside/pages', 'index.html')

        @self.app.route('/content/<path:path>')
        def serve_static(path):
            return send_from_directory('content', path)

    def serve(self):
        self.app.run()

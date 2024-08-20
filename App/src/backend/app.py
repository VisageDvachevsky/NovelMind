from flask import Flask, send_from_directory # type: ignore
import os
from .system_operations import system_ops_bp
from .file_operations import file_ops_bp

def create_app():
    app = Flask(__name__, static_folder='../Webview-interface/Editor/build')
    print("Static folder path:", os.path.abspath(app.static_folder))

    app.register_blueprint(system_ops_bp, url_prefix='/api/system')
    app.register_blueprint(file_ops_bp, url_prefix='/api/files')

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app
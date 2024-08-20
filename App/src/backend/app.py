import logging
from flask import Flask, jsonify, send_from_directory, request
from file_operations.routes import file_operations_bp
from system_operations.routes import system_operations_bp
import os

app = Flask(__name__, static_folder='../frontend/build')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app.register_blueprint(file_operations_bp, url_prefix='/file_operations')
app.register_blueprint(system_operations_bp, url_prefix='/system_operations')

@app.route('/')
def serve_react_app():
    logger.info("Serving React app")
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    logger.info(f"Serving static file: {path}")
    file_path = os.path.join(app.static_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        logger.warning(f"File not found: {path}, redirecting to React app")
        return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(e):
    logger.warning(f"404 error encountered, serving React app for path: {request.path}")
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    logger.info("Starting Flask server")
    app.run(debug=True)

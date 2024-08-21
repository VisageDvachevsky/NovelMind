import logging
from flask import Flask, jsonify
from flask_cors import CORS
from .system_operations import system_ops_bp
from .file_operations import file_ops_bp

def create_app():
    logging.basicConfig(level=logging.DEBUG, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    logger.debug("Initializing Flask app")
    
    app = Flask(__name__)
    CORS(app)
    

    logger.debug("Registering blueprints")
    app.register_blueprint(system_ops_bp, url_prefix='/api/system')
    app.register_blueprint(file_ops_bp, url_prefix='/api/files')

    logger.info("Flask app created successfully")
    return app
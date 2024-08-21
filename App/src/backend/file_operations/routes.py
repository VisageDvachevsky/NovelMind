import logging
from flask import Blueprint, request, jsonify
from .service import FileOperationsService

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

file_ops_bp = Blueprint('file_ops', __name__)
file_service = FileOperationsService()

def log_request_details():
    logger.debug(f"Request path: {request.path}")
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Request body: {request.get_json()}")

@file_ops_bp.route('/add_file', methods=['POST'])
def add_file():
    log_request_details()
    data = request.json
    file_path = data.get('file_path')
    file_id = data.get('file_id')

    try:
        logger.debug(f"Adding file with path: {file_path}, id: {file_id}")
        file_service.add_file(file_path, file_id)
        logger.info("File added successfully")
        return jsonify({"message": "File added successfully"}), 200
    except Exception as e:
        logger.error(f"Error adding file: {e}")
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/read_file', methods=['GET'])
def read_file():
    log_request_details()
    file_id = request.args.get('file_id')
    decode = request.args.get('decode', 'false').lower() == 'true'

    try:
        logger.debug(f"Reading file with id: {file_id}, decode: {decode}")
        content = file_service.read_file(file_id, decode)
        logger.info("File read successfully")
        return jsonify({"content": content}), 200
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/delete_file', methods=['DELETE'])
def delete_file():
    log_request_details()
    file_id = request.args.get('file_id')

    try:
        logger.debug(f"Deleting file with id: {file_id}")
        file_service.delete_file(file_id)
        logger.info("File deleted successfully")
        return jsonify({"message": "File deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/list_files', methods=['GET'])
def list_files():
    log_request_details()
    try:
        logger.debug("Listing all files")
        files = file_service.list_files()
        logger.info("Files listed successfully")
        return jsonify(files), 200
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/create_directory', methods=['POST'])
def create_directory():
    log_request_details()
    data = request.json
    dir_name = data.get('dir_name')

    try:
        logger.debug(f"Creating directory with name: {dir_name}")
        file_service.create_directory(dir_name)
        logger.info("Directory created successfully")
        return jsonify({"message": "Directory created successfully"}), 200
    except Exception as e:
        logger.error(f"Error creating directory: {e}")
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/rename_directory', methods=['PUT'])
def rename_directory():
    log_request_details()
    data = request.json
    old_name = data.get('old_name')
    new_name = data.get('new_name')

    try:
        logger.debug(f"Renaming directory from {old_name} to {new_name}")
        file_service.rename_directory(old_name, new_name)
        logger.info("Directory renamed successfully")
        return jsonify({"message": "Directory renamed successfully"}), 200
    except Exception as e:
        logger.error(f"Error renaming directory: {e}")
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/delete_directory', methods=['DELETE'])
def delete_directory():
    log_request_details()
    dir_name = request.args.get('dir_name')

    try:
        logger.debug(f"Deleting directory with name: {dir_name}")
        file_service.delete_directory(dir_name)
        logger.info("Directory deleted successfully")
        return jsonify({"message": "Directory deleted successfully"}), 200
    except Exception as e:
        logger.error(f"Error deleting directory: {e}")
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/move_file', methods=['PUT'])
def move_file():
    log_request_details()
    data = request.json
    file_id = data.get('file_id')
    dest_dir = data.get('dest_dir')

    try:
        logger.debug(f"Moving file with id: {file_id} to directory: {dest_dir}")
        file_service.move_file(file_id, dest_dir)
        logger.info("File moved successfully")
        return jsonify({"message": "File moved successfully"}), 200
    except Exception as e:
        logger.error(f"Error moving file: {e}")
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/change_directory', methods=['PUT'])
def change_directory():
    log_request_details()
    data = request.json
    dir_name = data.get('dir_name')

    try:
        logger.debug(f"Changing current directory to: {dir_name}")
        file_service.change_directory(dir_name)
        logger.info("Directory changed successfully")
        return jsonify({"message": "Directory changed successfully"}), 200
    except Exception as e:
        logger.error(f"Error changing directory: {e}")
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/current_directory', methods=['GET'])
def get_current_directory():
    log_request_details()
    try:
        logger.debug("Getting current directory")
        current_dir = file_service.get_current_directory()
        logger.info(f"Current directory: {current_dir}")
        return jsonify({"current_directory": current_dir}), 200
    except Exception as e:
        logger.error(f"Error getting current directory: {e}")
        return jsonify({"error": str(e)}), 400

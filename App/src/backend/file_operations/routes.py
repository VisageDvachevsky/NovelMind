import logging
from flask import Blueprint, request, jsonify
from .service import FileOperations, SecureFileHandler

file_operations_bp = Blueprint('file_operations', __name__)

logger = logging.getLogger(__name__)

file_handler = SecureFileHandler(base_path='/path/to/files', master_password='your_password')
file_operations = FileOperations(file_handler)

@file_operations_bp.route('/add', methods=['POST'])
def add_file():
    file_path = request.form['file_path']
    file_id = request.form['file_id']
    logger.info(f"Adding file: {file_path} with id: {file_id}")
    try:
        file_operations.add_file(file_path, file_id)
        return jsonify({"status": "File added successfully"}), 200
    except Exception as e:
        logger.error(f"Failed to add file {file_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@file_operations_bp.route('/read', methods=['GET'])
def read_file():
    file_id = request.args.get('file_id')
    decode = request.args.get('decode', 'false').lower() == 'true'
    logger.info(f"Reading file: {file_id} with decode={decode}")
    try:
        content = file_operations.read_file(file_id, decode)
        return jsonify({"content": content}), 200
    except FileNotFoundError:
        logger.error(f"File {file_id} not found")
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        logger.error(f"Failed to read file {file_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@file_operations_bp.route('/delete', methods=['POST'])
def delete_file():
    file_id = request.form['file_id']
    logger.info(f"Deleting file: {file_id}")
    try:
        file_operations.delete_file(file_id)
        return jsonify({"status": "File deleted successfully"}), 200
    except FileNotFoundError:
        logger.error(f"File {file_id} not found")
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        logger.error(f"Failed to delete file {file_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@file_operations_bp.route('/list', methods=['GET'])
def list_files():
    logger.info("Listing all files")
    try:
        files = file_operations.list_files()
        return jsonify(files), 200
    except Exception as e:
        logger.error(f"Failed to list files: {str(e)}")
        return jsonify({"error": str(e)}), 500

@file_operations_bp.route('/create_directory', methods=['POST'])
def create_directory():
    dir_name = request.form['dir_name']
    logger.info(f"Creating directory: {dir_name}")
    try:
        file_operations.create_directory(dir_name)
        return jsonify({"status": "Directory created successfully"}), 200
    except Exception as e:
        logger.error(f"Failed to create directory {dir_name}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@file_operations_bp.route('/rename_directory', methods=['POST'])
def rename_directory():
    old_name = request.form['old_name']
    new_name = request.form['new_name']
    logger.info(f"Renaming directory from {old_name} to {new_name}")
    try:
        file_operations.rename_directory(old_name, new_name)
        return jsonify({"status": "Directory renamed successfully"}), 200
    except FileNotFoundError:
        logger.error(f"Directory {old_name} not found")
        return jsonify({"error": "Directory not found"}), 404
    except Exception as e:
        logger.error(f"Failed to rename directory {old_name}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@file_operations_bp.route('/delete_directory', methods=['POST'])
def delete_directory():
    dir_name = request.form['dir_name']
    logger.info(f"Deleting directory: {dir_name}")
    try:
        file_operations.delete_directory(dir_name)
        return jsonify({"status": "Directory deleted successfully"}), 200
    except FileNotFoundError:
        logger.error(f"Directory {dir_name} not found")
        return jsonify({"error": "Directory not found"}), 404
    except Exception as e:
        logger.error(f"Failed to delete directory {dir_name}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@file_operations_bp.route('/move_file', methods=['POST'])
def move_file():
    file_id = request.form['file_id']
    dest_dir = request.form['dest_dir']
    logger.info(f"Moving file: {file_id} to directory: {dest_dir}")
    try:
        file_operations.move_file(file_id, dest_dir)
        return jsonify({"status": "File moved successfully"}), 200
    except FileNotFoundError:
        logger.error(f"File {file_id} or directory {dest_dir} not found")
        return jsonify({"error": "File or directory not found"}), 404
    except Exception as e:
        logger.error(f"Failed to move file {file_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@file_operations_bp.route('/change_directory', methods=['POST'])
def change_directory():
    dir_name = request.form['dir_name']
    logger.info(f"Changing directory to: {dir_name}")
    try:
        file_operations.change_directory(dir_name)
        return jsonify({"status": "Directory changed successfully", "current_directory": file_operations.get_current_directory()}), 200
    except FileNotFoundError:
        logger.error(f"Directory {dir_name} not found")
        return jsonify({"error": "Directory not found"}), 404
    except Exception as e:
        logger.error(f"Failed to change directory to {dir_name}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@file_operations_bp.route('/current_directory', methods=['GET'])
def get_current_directory():
    logger.info("Getting current directory")
    try:
        current_directory = file_operations.get_current_directory()
        return jsonify({"current_directory": current_directory}), 200
    except Exception as e:
        logger.error(f"Failed to get current directory: {str(e)}")
        return jsonify({"error": str(e)}), 500

from flask import Blueprint, request, jsonify # type: ignore
from .service import FileOperationsService

file_ops_bp = Blueprint('file_ops', __name__)
file_service = FileOperationsService()

@file_ops_bp.route('/add_file', methods=['POST'])
def add_file():
    data = request.json
    file_path = data.get('file_path')
    file_id = data.get('file_id')
    
    try:
        file_service.add_file(file_path, file_id)
        return jsonify({"message": "File added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/read_file', methods=['GET'])
def read_file():
    file_id = request.args.get('file_id')
    decode = request.args.get('decode', 'false').lower() == 'true'
    
    try:
        content = file_service.read_file(file_id, decode)
        return jsonify({"content": content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/delete_file', methods=['DELETE'])
def delete_file():
    file_id = request.args.get('file_id')
    
    try:
        file_service.delete_file(file_id)
        return jsonify({"message": "File deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/list_files', methods=['GET'])
def list_files():
    try:
        files = file_service.list_files()
        return jsonify(files), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/create_directory', methods=['POST'])
def create_directory():
    data = request.json
    dir_name = data.get('dir_name')
    
    try:
        file_service.create_directory(dir_name)
        return jsonify({"message": "Directory created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/rename_directory', methods=['PUT'])
def rename_directory():
    data = request.json
    old_name = data.get('old_name')
    new_name = data.get('new_name')
    
    try:
        file_service.rename_directory(old_name, new_name)
        return jsonify({"message": "Directory renamed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/delete_directory', methods=['DELETE'])
def delete_directory():
    dir_name = request.args.get('dir_name')
    
    try:
        file_service.delete_directory(dir_name)
        return jsonify({"message": "Directory deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/move_file', methods=['PUT'])
def move_file():
    data = request.json
    file_id = data.get('file_id')
    dest_dir = data.get('dest_dir')
    
    try:
        file_service.move_file(file_id, dest_dir)
        return jsonify({"message": "File moved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/change_directory', methods=['PUT'])
def change_directory():
    data = request.json
    dir_name = data.get('dir_name')
    
    try:
        file_service.change_directory(dir_name)
        return jsonify({"message": "Directory changed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@file_ops_bp.route('/current_directory', methods=['GET'])
def get_current_directory():
    try:
        current_dir = file_service.get_current_directory()
        return jsonify({"current_directory": current_dir}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
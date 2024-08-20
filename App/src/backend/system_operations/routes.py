from flask import Blueprint, request, jsonify
from .service import SystemOperationsService

system_ops_bp = Blueprint('system_ops', __name__)

@system_ops_bp.route('/deploy', methods=['POST'])
def deploy():
    data = request.json
    base_path = data.get('base_path')
    master_password = data.get('master_password')
    
    try:
        SystemOperationsService.deploy(base_path, master_password)
        return jsonify({"message": "System deployed successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
import logging
from flask import Blueprint, request, jsonify
from .service import SystemOperations

system_operations_bp = Blueprint('system_operations', __name__)

logger = logging.getLogger(__name__)

@system_operations_bp.route('/deploy', methods=['POST'])
def deploy_system():
    base_path = request.form['base_path']
    master_password = request.form['master_password']
    logger.info(f"Deploying system at base path: {base_path}")
    try:
        file_handler = SystemOperations.deploy(base_path, master_password)
        return jsonify({"status": "System deployed successfully"}), 200
    except ValueError as ve:
        logger.error(f"Failed to deploy system due to invalid path: {str(ve)}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Failed to deploy system: {str(e)}")
        return jsonify({"error": str(e)}), 500


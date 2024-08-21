from flask import Blueprint, request, jsonify # type: ignore
from .service import SystemOperationsService
import os
import logging

logger = logging.getLogger(__name__)

system_ops_bp = Blueprint('system_ops', __name__)

@system_ops_bp.route('/deploy', methods=['POST'])
def deploy():
    logger.debug(f"Received POST request on /deploy with body: {request.json}")
    data = request.json
    base_path = data.get('base_path')
    master_password = data.get('master_password')

    try:
        logger.debug(f"Deploying system at base path: {base_path}")
        os.chdir(base_path)
        SystemOperationsService.deploy(base_path, master_password)
        logger.info("System deployed successfully")
        return jsonify({"message": "System deployed successfully"}), 200
    except ValueError as e:
        logger.error(f"Deployment error: {e}")
        return jsonify({"error": str(e)}), 400

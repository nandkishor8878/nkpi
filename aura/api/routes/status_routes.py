from flask import Blueprint, jsonify

from aura.api.routes._container import get_container


status_bp = Blueprint("status", __name__, url_prefix="/api/v1")


@status_bp.get("/status")
def robot_status():
    container = get_container()
    return jsonify(container.robot_status_service.get_status())
